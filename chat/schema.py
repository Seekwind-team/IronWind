import graphene
from graphene_django import DjangoObjectType
from graphene_subscriptions.events import CREATED
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from rx import Observable

from chat.models import Message
from user.models import Authentication


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class AuthType(DjangoObjectType):
    class Meta:
        model = Authentication
        fields = ('id',)


class Subscription(graphene.ObjectType):
    count_seconds = graphene.Int(up_to=graphene.Int())

    def resolve_count_seconds(
            self,
            info,
            up_to=5
    ):
        return Observable.interval(1000) \
            .map(lambda i: "{0}".format(i)) \
            .take_while(lambda i: int(i) <= up_to)

    message_created = graphene.Field(MessageType)

    def resolve_message_created(root, info):
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
        message = Message(
            sender=info.context.user,
            receiver=receiver_obj,
            message=message
        )
        message.save()
        post_save.connect(
            post_save_subscription, sender=Message, dispatch_uid="some_model_post_save"
        )
        return SendMessage(ok=True)


class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()


class Query(graphene.ObjectType):
    get_messages = graphene.List(MessageType, partner=graphene.Int())
    get_chats = graphene.List(MessageType)

    @login_required
    def resolve_get_messages(self, info, partner):
        pass

    @login_required
    def resolve_get_chats(self, info):
        return Message.objects.filter(Q(sender=info.context.user) | Q(sender=info.context.user))
    #    a.append(Message.objects.filter(receiver=info.context.user).query.group_by('sender'))
    #    return a

