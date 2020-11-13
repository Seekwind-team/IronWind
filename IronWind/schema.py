import graphene
import graphql_jwt
import user.schema


# put here any Queries to inherit them
class Query(user.schema.Query, graphene.ObjectType):
    # Demo- Shit
    ping = graphene.String(default_value="Pong")
    hallo = graphene.String(name=graphene.String(default_value="Fremder"))

    def resolve_hallo(root, info, name):
        return f'Guten Morgen, {name}!'


# put here any Mutations to inherit them
class Mutation(user.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token = graphql_jwt.DeleteJSONWebTokenCookie()


schema = graphene.Schema(query=Query, mutation=Mutation)
