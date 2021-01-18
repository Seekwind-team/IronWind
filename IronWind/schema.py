import graphene
import graphql_jwt
from django.utils import timezone
from graphene.types import datetime
from graphql_jwt.decorators import setup_jwt_cookie, csrf_rotation, refresh_expiration, on_token_auth_resolve
from functools import wraps
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from graphene.utils.thenables import maybe_thenable
from graphql_jwt import exceptions, signals
from django.contrib.auth import get_user_model


import carespace.schema
import chat.schema
import joboffer.schema
import user.schema
import recommenders.schema


# Overwrites tokenAuth decorator to always interpret given username as lowercase
def token_auth(f):
    @wraps(f)
    @setup_jwt_cookie
    @csrf_rotation
    @refresh_expiration
    def wrapper(cls, root, info, password, **kwargs):
        context = info.context
        context._jwt_token_auth = True
        username = kwargs.get(get_user_model().USERNAME_FIELD).lower()

        user = authenticate(
            request=context,
            username=username,
            password=password,
        )
        if user is None:
            raise exceptions.JSONWebTokenError(
                _('Please enter valid credentials'),
            )

        if hasattr(context, 'user'):
            context.user = user

        result = f(cls, root, info, **kwargs)
        signals.token_issued.send(sender=cls, request=context, user=user)
        return maybe_thenable((context, user, result), on_token_auth_resolve)
    return wrapper


class ObtainJSONWebToken(graphql_jwt.ObtainJSONWebToken):
    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({
            get_user_model().USERNAME_FIELD: graphene.String(required=True),
            'password': graphene.String(required=True),
        })
        return super().Field(*args, **kwargs)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)


# put here any Queries to inherit them
class Query(carespace.schema.Query, chat.schema.Query,recommenders.schema.Query, joboffer.schema.Query, user.schema.Query, graphene.ObjectType):
    # Method that Simply returns 'Pong'
    ping = graphene.String(default_value="Pong", description="Used internally for testing, will return \"Pong\"")
    # Returns current Server Time
    get_server_time = graphene.DateTime(description="Will return server time, aligned with all times stamps")

    def resolve_get_server_time(self, info):
        return timezone.now()


# put here any Mutations to inherit them
class Mutation(joboffer.schema.Mutation, user.schema.Mutation, chat.schema.Mutation):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token = graphql_jwt.DeleteJSONWebTokenCookie()


class Subscription(chat.schema.Subscription, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, types=[], subscription=Subscription,)

