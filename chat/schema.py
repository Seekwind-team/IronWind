import django.db.models.signals
import graphene
import graphene_subscriptions.signals
from graphene_django import DjangoObjectType
from graphene_subscriptions.events import CREATED
from django.db.models import Q
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from rx import Observable

from graphql_jwt import mixins

from chat.models import Message
from user.models import Authentication
from user.schema import UserType

import IronWind.schema


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class Subscription(graphene.ObjectType):
    count_seconds = graphene.Int(
        up_to=graphene.Int(description="Seconds the Observable Object will count to. Used for Internal testing"),
        description="Simple Method that counts up to a given value. Used for Internal testing only")

    def resolve_count_seconds(
            self,
            info,
            up_to=5
    ):
        return Observable.interval(1000) \
            .map(lambda i: "{0}".format(i)) \
            .take_while(lambda i: int(i) <= up_to)

    message_created = graphene.Field(MessageType,
                                     token=graphene.String(required=True),
                                     description="creates an observable to receive all messages sent to logged in user",
                                     )

    def resolve_message_created(self, info, *args, token, **kwargs):
        """creates an observable to receive all messages sent to logged in user"""

        # this is a REALLY shitty workaround, see https://github.com/flavors/django-graphql-jwt/issues/239 for any
        # development of the roots issue
        schema = graphene.Schema(mutation=IronWind.schema.Mutation)

        result = schema.execute(
            '''
                mutation testMutation($token:String!){
                    verifyToken(token: $token) {
                        payload
                    }
                }
            ''', variables={'token': token},
        )
        print(result)
        email = result.data['verifyToken']['payload']['email']

        receiver = Authentication.objects.filter(email=email).get()

        # checks validity of the messages receiver
        def check_validity_and_modify(event, rec):
            if event.instance.receiver.id is rec.pk:
                # room to do something with the message object
                return True
            return False

        return self.filter(
            lambda event:
            event.operation == CREATED and
            isinstance(event.instance, Message) and (check_validity_and_modify(event, receiver))
        ).map(lambda event: event.instance)


class SendMessage(graphene.Mutation):
    """Function Used to send a message to selected recipient"""
    ok = graphene.Boolean()

    class Arguments:
        receiver_id = graphene.Int(required=True, description="ID of the receiver of this message")
        message = graphene.String(required=True, description="content of this message")

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
            graphene_subscriptions.signals.post_save_subscription, sender=Message, dispatch_uid="message_pre_save"
        )
        message.save()
        return SendMessage(ok=True)


class SetRead(graphene.Mutation):

    ok = graphene.Boolean()

    class Arguments:
        message_ids = graphene.List(graphene.Int, required=True, description= "Message" )

    def mutate(self, info, message_ids):
        for message_id in message_ids:
            obj = Message.objects.filter(pk=message_id).get()
            if obj.receiver.id is info.context.user.id:
                obj.unread = False
                obj.save()
            else:
                raise GraphQLError('can\'t mark messages not directed to current user as \'read\'')

        return SetRead(ok=True)


class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()
    set_read = SetRead.Field()


class Query(graphene.ObjectType):
    get_messages = graphene.List(
        MessageType,
        partner=graphene.Int(description="ID of partner messages are loaded on"),
        n_from=graphene.Int(
            description="selects messages from n, where 0 ist the last message received. Defaults to 0"),
        n_to=graphene.Int(description="will return n last messages, defaults to 25"),
        description="Function Used to get n-last messages with stated partner"
    )
    get_chats = graphene.List(
        MessageType,
        description="Returns all partners that logged in user has a chat-history with"
    )

    @login_required
    def resolve_get_messages(self, info, partner, n_from=0, n_to=25):
        """Function Used to get n-last messages with stated partner"""
        messages_loaded = Message.objects \
                              .filter(Q(sender=info.context.user) or Q(receiver=info.context.user)) \
                              .filter(Q(receiver=partner) or Q(sender=partner)) \
                              .all().order_by('timestamp').reverse()[n_from:n_to]
        return messages_loaded

    @login_required
    def resolve_get_chats(self, info):
        """Function Used to get all partners that logged in user has a chat-history with"""
        partners = set()
        last_messages = set()
        for e in Message.objects.filter(Q(sender=info.context.user) or Q(receiver=info.context.user)).all():
            if e.receiver is not info.context.user:
                partners.add(e.receiver)
            if e.sender is not info.context.user:
                partners.add(e.sender)

        print(partners)
        for partner in partners:
            print(partner)
            last_message = Message.objects\
                .filter(Q(receiver=info.context.user) or Q(sender=info.context.user))\
                .filter(Q(receiver=partner) or Q(sender=partner)).last()
            print(last_message)
            last_messages.add(last_message)

        return last_messages
