import graphene
from graphene_django import DjangoObjectType
from graphene_subscriptions.events import CREATED
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from rx import Observable

from chat.models import Message
from user.models import Authentication


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())

    def resolve_count_seconds(
        self,
        info,
        up_to=5
    ):
        return Observable.interval(1000)\
                            .map(lambda i: "{0}".format(i))\
                            .take_while(lambda i: int(i) <= up_to)

    await_message = graphene.Field(MessageType)

    def resolve_await_message(root, info):
        return root.filter(
            lambda event:
                event.operation == CREATED and
                isinstance(event.instance, Message)
        ).map(lambda event: event.instance)


class SendMessage(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        receiver_id = graphene.Int(required=True)
        message = graphene.String(required=True)

    @login_required
    def mutate(self, info, receiver_id, message):

        try:
            receiver_obj = Authentication.objects.filter(pk=receiver_id).get()
        except Exception as e:
            raise GraphQLError('Can\'t resolve receiver!', e)
        Message(
            sender=info.context.user,
            receiver=receiver_obj,
            message=message
        )
        return SendMessage(ok=True)


class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()



