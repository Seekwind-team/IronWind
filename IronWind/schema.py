import graphene
import graphql_jwt
from django.utils import timezone

import joboffer.schema
import user.schema
import recommenders.schema

from django.contrib.auth import get_user_model


# put here any Queries to inherit them
class Query(recommenders.schema.Query, joboffer.schema.Query, user.schema.Query, graphene.ObjectType):
    # Demo- Shit
    ping = graphene.String(default_value="Pong")
    get_server_time = graphene.DateTime()

    def resolve_get_server_time(self, info, name):
        return timezone.now()


# put here any Mutations to inherit them
class Mutation(joboffer.schema.Mutation, user.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token = graphql_jwt.DeleteJSONWebTokenCookie()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[])
