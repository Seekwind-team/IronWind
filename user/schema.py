from django.contrib.auth import get_user_model

import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        try:
            validate_email(email)
        except ValidationError as e:
            raise Exception("invalid email address, ",e)
        else:
            user = get_user_model().objects.create_user(
                email=email,
                password=password
            )
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
