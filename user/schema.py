from django.contrib.auth import get_user_model

import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = get_user_model()(
            email=email,
            is_superuser=True,
            is_staff=True,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    users_by_id = graphene.Field(UserType, id=graphene.Int())

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        return info.context.user

    @login_required
    def resolve_users_by_id(self, info, id):
        return get_user_model().objects.get(pk=id)
