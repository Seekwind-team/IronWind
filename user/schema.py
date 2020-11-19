from django.contrib.auth import get_user_model

import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required, user_passes_test
from graphene_django import DjangoObjectType
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from user.models import UserData, CompanyData


# To Check whether a user is on a company account or not
def is_company(user):
    return user.is_company is True


# Imports User Profile from Models
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        description = 'Returns auth data data'
        exclude_fields = ('password', 'is_superuser')


# Imports UserData from Models
class UserDataType(DjangoObjectType):
    class Meta:
        model = UserData


# Imports ComapnyData from Models
class CompanyDataType(DjangoObjectType):
    class Meta:
        model = CompanyData


# Deletes currently logged in account
class DeleteUser(graphene.Mutation):
    # returns boolean indicating success of the operation
    ok = graphene.Boolean()

    class Arguments:
        # requires password authentication for the process
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
        email = graphene.String(required=True, description="EMail Used to authenticate user, must be unique")
        password = graphene.String(required=True, description="Password on account creation")
        is_company = graphene.Boolean(required=True, description="Set to True, if account created is for a company, "
                                                                 "set to false otherwise")

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
        first_name = graphene.String(description="first name")
        last_name = graphene.String(description="last name")
        phone_number = graphene.String(description="phone number of user, uses E.165-Format")
        short_bio = graphene.String(description="short bio (self description) of user, 5000 characters maximum")
        gender = graphene.String(description="gender of user")
        birth_date = graphene.Date(description="birthdate of user, uses iso8601-Format (eg. 2006-01-02)")

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
        company_name = graphene.String(description="name of company")
        description = graphene.String(description="description of company, max. 5000 characters")
        phone_number = graphene.String(description="phone number of the HR manager E.165-Format")
        last_name = graphene.String(description="last name of HR manager")
        first_name = graphene.String(description="first name of HR manager")
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


# Read functions for all Profiles
class Query(graphene.AbstractType):
    me = graphene.Field(UserType)

    # my_company = graphene.Field(CompanyDataType) # not needed, see giant comment below
    # my_user = graphene.Field(UserDataType) # not needed, see giant comment below

    # returns auth data
    @login_required # would return an error on 'Anonymous user', so restricting this to authenticated users
    def resolve_me(self, info):
        return info.context.user

    # those functions below aren't actually used because I figured they are are unnecessary as all information they
    # provide can already be acquired though other means using the 'me'-Query, yet I am leaving this code in there for
    # now as they provide a reference on how things could be implemented

    # return company profile (requires company boolean to be set 'true')
    @login_required
    @user_passes_test(lambda user: is_company(user))
    def resolve_my_company(self, info):
        if not CompanyData.objects.filter(belongs_to=info.context.user):
            user_data = CompanyData(
                belongs_to=info.context.user
            )
            user_data.save()
        return CompanyData.objects.filter(belongs_to=info.context.user).get()

    # return company profile (requires company boolean to be set 'false')
    @login_required
    @user_passes_test(lambda user: not is_company(user))
    def resolve_my_user(self, info):
        if not UserData.objects.filter(belongs_to=info.context.user):
            user_data = UserData(
                belongs_to=info.context.user
            )
            user_data.save()
        return UserData.objects.filter(belongs_to=info.context.user).get()
