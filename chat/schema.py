import django.db.models.signals
import graphene
import graphene_subscriptions.signals
from graphene_django import DjangoObjectType
from graphene_subscriptions.events import CREATED
from django.db.models import Q
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from rx import Observable

from chat.models import Message
from user.models import Authentication
from user.schema import UserType


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
        django.db.models.signals.post_save.connect(
            graphene_subscriptions.signals.post_save_subscription, sender=Message, dispatch_uid="message_post_save"
        )
        message.save()
        return SendMessage(ok=True)


class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()


class Query(graphene.ObjectType):
    get_messages = graphene.List(MessageType, partner=graphene.Int(), n_from=graphene.Int(), n_to=graphene.Int())
    # get_chats = graphene.List(MessageType)
    get_chats = graphene.List(UserType)

    @login_required
    def resolve_get_messages(self, info, partner, n_from=0, n_to=25):
        return Message.objects\
            .filter(Q(sender=info.context.user) | Q(receiver=info.context.user))\
            .filter(Q(receiver=partner) | Q(sender=partner))\
            .all().order_by('timestamp').reverse()[n_from:n_to]

    @login_required
    def resolve_get_chats(self, info):
        partners = set()
        for e in Message.objects.filter(Q(sender=info.context.user) | Q(receiver=info.context.user)).all():
            if e.receiver is not info.context.user:
                partners.add(e.receiver)
            if e.sender is not info.context.user:
                partners.add(e.sender)
        return partners


