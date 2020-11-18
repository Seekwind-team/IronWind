
from django.contrib.auth import get_user_model

import graphene
import graphql_jwt
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

# Deletes currently logged in account
class DeleteUser(graphene.Mutation):

    # returns boolean indicating success of the operation
    ok = graphene.Boolean()

    class Arguments:
        # requires password authentification for the process
        password = graphene.String(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        # checks whether provided password is correct
        if user.check_password(raw_password=kwargs["password"]):
            user.delete()
            return DeleteUser(ok=True)
        else:
            raise Exception("wrong password provided")
        return DeleteUser(ok=False)


# creates new User profile
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


# Updates Profile with non-sensitive content (eg. password and email is left out on purpose as they demand password
# verification and are therefore handled separately)
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
               first_name=None,  # setting default values to none
               last_name=None,  # they will be replaced through input and won't overwrite actual userdata
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


# Used to Update Company Profiles
class UpdatedCompany(graphene.Mutation):

    updated_profile = graphene.Field(CompanyDataType)

    class Arguments:
        company_name = graphene.String()
        description = graphene.String()
        phone_number = graphene.String()
        last_name = graphene.String()
        first_name = graphene.String()
        # company_picture = #TODO Picture??
        # meisterbrief #TODO Picture??

    @login_required  # requires login
    @user_passes_test(lambda user: is_company(user))
    def mutate(self, info,
               company_name=None,
               description=None,
               phone_number=None,
               first_name=None,
               last_name=None):

        # creates new Database entry, if none exists
        if not CompanyData.objects.filter(belongs_to=info.context.user):
            company_data = CompanyData(
                belongs_to=info.context.user
            )
            company_data.save()

        # Grabs the entry from the Database belonging to current User
        data_object = CompanyData.objects.filter(belongs_to=info.context.user).get()
        data_object.phone_number = phone_number or data_object.data_object
        data_object.description = description or data_object.description
        data_object.company_name = company_name or data_object.company_name
        data_object.last_name = last_name or data_object.last_name
        data_object.first_name = first_name or data_object.first_name
        data_object.save()

        return UpdatedCompany(updated_profile=data_object)


# Create - Update - Delete for all User-Profiles
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdatedProfile.Field()
    update_company = UpdatedCompany.Field()
    delete_user = DeleteUser.Field()


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
