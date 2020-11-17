from django.contrib.auth import get_user_model

import graphene
from graphql_jwt.decorators import login_required, user_passes_test
from graphene_django import DjangoObjectType
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from user.models import UserData, CompanyData


# To Check whether a user is on a company accout or not
def is_company(user):
    return user.is_company is True


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserDataType(DjangoObjectType):
    class Meta:
        model = UserData


class CompanyDataType(DjangoObjectType):
    class Meta:
        model = CompanyData


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        is_company = graphene.Boolean(required=True)

    def mutate(self, info, email, password, is_company=False):
        try:
            validate_email(email)
        except ValidationError as e:
            raise Exception("invalid email address, ", e)
        else:
            user = get_user_model()(email=email.lower())
            user.set_password(password)
            user.is_company = is_company
            user.save()

            return CreateUser(user=user)


class UpdatedProfile(graphene.Mutation):
    updated_profile = graphene.Field(UserDataType)

    # accepted arguments from mutation
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        phone_number = graphene.String()
        short_bio = graphene.String()
        gender = graphene.String()
        birth_date = graphene.Date()

    @login_required  # requires login
    @user_passes_test(lambda user: not is_company(user))  # only applicable for non-company accounts
    def mutate(self, info,
               first_name=None,
               last_name=None,
               phone_number=None,
               short_bio=None,
               gender=None,
               birth_date=None):

        # creates new Database entry, if none exists
        if not UserData.objects.filter(belongs_to=info.context.user):
            user_data = UserData(
                belongs_to=info.context.user
            )
            user_data.save()

        # Grabs the entry from the Database belonging to current User
        data_object = UserData.objects.filter(belongs_to=info.context.user).get()

        # overwrites all Not-None-Values
        data_object.first_name = first_name or data_object.first_name
        data_object.last_name = last_name or data_object.last_name
        data_object.phone_number = phone_number or data_object.phone_number
        data_object.short_bio = short_bio or data_object.short_bio
        data_object.gender = gender or data_object.gender
        data_object.birth_date = birth_date or data_object.birth_date
        data_object.save()

        return UpdatedProfile(updated_profile=data_object)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdatedProfile.Field()


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    users_by_id = graphene.Field(UserType, id=graphene.Int())

    @login_required
    def resolve_users(self, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @login_required
    def resolve_users_by_id(self, info, id):
        return get_user_model().objects.get(pk=id)
