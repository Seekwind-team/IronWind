import os

from django.contrib.auth import get_user_model

import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required, user_passes_test, token_auth
from graphene_django import DjangoObjectType

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from user.models import UserData, CompanyData, SoftSkills


class Upload(graphene.types.Scalar):
    """Create scalar that ignores normal serialization/deserialization, since
    that will be handled by the multipart request spec"""

    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value


# To Check whether a user is on a company account or not
def is_company(user):
    return user.is_company is True


# Imports User Profile from Models
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        description = 'Returns auth data'
        exclude_fields = ('password', 'is_superuser', 'message_sender', 'message_receiver')


# Imports UserData from Models
class UserDataType(DjangoObjectType):
    class Meta:
        model = UserData
        description = 'This Type contains a singular set of User-Data'


# Imports CompanyData from Models
class CompanyDataType(DjangoObjectType):
    class Meta:
        model = CompanyData
        description = 'This Type contains a singular set of Company-Data'

class SoftSkillsType(DjangoObjectType):
    class Meta:
        model = SoftSkills
        description = 'This Type contains slider values from -5 to 5 for Softskills'

# Deletes currently logged in account
class DeleteUser(graphene.Mutation):
    # returns boolean indicating success of the operation
    ok = graphene.Boolean(description="returns true on successful operation")

    class Arguments:
        # requires password authentication for the process
        password = graphene.String(required=True,
                                   description="Must provide valid password for user to delete own account")

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        # checks whether provided password is correct
        if user.check_password(raw_password=kwargs["password"]):
            try:
                if user.is_company:
                    data = CompanyData.objects.filter(belongs_to=user).get()
                    if data.company_picture:
                        data.company_picture.storage.delete(data.company_picture.name)
                else:
                    data = UserData.objects.filter(belongs_to=user).get()
                    if data.profile_picture:
                        data.profile_picture.storage.delete(data.profile_picture.name)
            # Not a real error, only means user hasn't updated profile with any information yet
            except Exception:
                None

            user.delete()
            return DeleteUser(ok=True)
        else:
            raise GraphQLError("wrong password provided")
        return DeleteUser(ok=False)


class SoftSkillsArguments(graphene.InputObjectType):
    artistic = graphene.Int()
    social_activity = graphene.Int()
    customer_orientated =graphene.Int()
    motorskills =graphene.Int()
    planning = graphene.Int()
    empathic =graphene.Int()
    creativity =graphene.Int()
    digital = graphene.Int()
    innovativity = graphene.Int()
    early_rise = graphene.Int()
    routine = graphene.Int()
    communicativity = graphene.Int()


# creates new User profile
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType, description="returns user created")

    class Arguments:
        email = graphene.String(required=True, description="EMail Used to authenticate user, must be unique")
        password = graphene.String(required=True, description="Password on account creation")
        is_company = graphene.Boolean(required=True,
                                      description="Set to True, if account created is for a company, set to false otherwise")

    def mutate(self, info, email, password, is_company=False):
        try:
            validate_email(email)
        except ValidationError as e:
            raise GraphQLError("invalid email address, ", e)
        else:
            user = get_user_model()(email=email.lower())
            user.set_password(password)
            user.is_company = is_company
            user.save()

            return CreateUser(user=user)


# Updates Profile with non-sensitive content (eg. password and email is left out on purpose as they demand password
# verification and are therefore handled separately)
class UpdatedProfile(graphene.Mutation):
    updated_profile = graphene.Field(UserDataType, description="returns updated user profile")

    # accepted arguments from mutation
    class Arguments:
        first_name = graphene.String(description="first name")
        last_name = graphene.String(description="last name")
        phone_number = graphene.String(description="phone number of user, uses E.165-Format")
        short_bio = graphene.String(description="short bio (self description) of user, 5000 characters maximum")
        gender = graphene.String(description="gender of user")
        birth_date = graphene.Date(description="birthdate of user, uses iso8601-Format (eg. 2006-01-02)")
        #  profile_picture = Upload(description="Uploaded File") #
        # TODO:
        soft_skills = graphene.Argument(SoftSkillsArguments,
            description="List of slider values for softskills. eg. \"creativity\":2"
        )

    @login_required  # requires login
    @user_passes_test(lambda user: not is_company(user))  # only applicable for non-company accounts
    def mutate(self, info,
               first_name=None,  # setting default values to none
               last_name=None,  # they will be replaced through input and won't overwrite actual userdata
               phone_number=None,
               short_bio=None,
               gender=None,
               birth_date=None,
               soft_skills=None):
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

        soft_skills_object = SoftSkills()
        soft_skills_object.artistic = soft_skills.artistic
        soft_skills_object.social_activity = soft_skills.social_activity
        soft_skills_object.customer_orientated = soft_skills.customer_orientated
        soft_skills_object.motorskills = soft_skills.motorskills
        soft_skills_object.planning = soft_skills.planning
        soft_skills_object.empathic = soft_skills.empathic
        soft_skills_object.creativity = soft_skills.creativity
        soft_skills_object.digital = soft_skills.digital
        soft_skills_object.innovativity = soft_skills.innovativity
        soft_skills_object.early_rise = soft_skills.early_rise
        soft_skills_object.routine = soft_skills.routine
        soft_skills_object.communicativity = soft_skills.communicativity
        soft_skills_object.save()
        
        data_object.soft_skills = soft_skills_object
        data_object.save()

        return UpdatedProfile(updated_profile=data_object)


class ChangePassword(graphene.Mutation):
    ok = graphene.Boolean(description="returns true on successful operation")

    class Arguments:
        old_password = graphene.String(description='Requires valid (old) password')
        new_password = graphene.String(description='new password to be set')

    @login_required
    def mutate(self, info, **kwargs):
        if info.context.user.check_password(kwargs['old_password']):
            info.context.user.set_password(kwargs['new_password'])
            info.context.user.save()
            return ChangePassword(ok=True)
        else:
            raise GraphQLError('wrong password submitted!')
        return ChangePassword(ok=False)


class ChangeEmail(graphene.Mutation):
    ok = graphene.Boolean(description="returns true on successful operation")

    class Arguments:
        password = graphene.String(description='Requires valid user-password')
        new_email = graphene.String(description='new email, must be provided in valid format')

    @login_required
    def mutate(self, info, **kwargs):
        if info.context.user.check_password(kwargs['password']):
            try:
                validate_email(kwargs['new_email'])
            except ValidationError as e:
                raise GraphQLError("must provide valid email address, ", e)
            info.context.user.email = kwargs['new_email']
            info.context.user.save()
            return ChangeEmail(ok=True)
        else:
            raise GraphQLError('wrong password submitted!')
        return ChangeEmail(ok=False)


# Used to Update Company Profiles
class UpdatedCompany(graphene.Mutation):
    updated_profile = graphene.Field(CompanyDataType, description="returns updated company profile")

    class Arguments:
        company_name = graphene.String(description="name of company")
        description = graphene.String(description="description of company, max. 5000 characters")
        phone_number = graphene.String(description="phone number of the HR manager E.165-Format")
        last_name = graphene.String(description="last name of HR manager")
        first_name = graphene.String(description="first name of HR manager")
        # company_picture =
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
        data_object.phone_number = phone_number or data_object.phone_number
        data_object.description = description or data_object.description
        data_object.company_name = company_name or data_object.company_name
        data_object.last_name = last_name or data_object.last_name
        data_object.first_name = first_name or data_object.first_name
        data_object.save()

        return UpdatedCompany(updated_profile=data_object)


class UploadUserPicture(graphene.Mutation):
    class Arguments:
        file_in = Upload(required=True, description="Uploaded File")

    ok = graphene.Boolean(description="returns true on successful operation")

    @login_required
    def mutate(self, info, file_in, **kwargs):
        # do something with your file
        c_user = info.context.user

        if file_in.content_type not in ['image/jpg', 'image/jpeg', "image/png"]:
            raise GraphQLError("Provided invalid file format")

        extension = os.path.splitext(file_in.name)[1]
        file_in.name = "" + str(c_user.pk) + "_profilePicture" + extension

        if c_user.is_company:
            if not CompanyData.objects.filter(belongs_to=info.context.user):
                company_data = CompanyData(
                    belongs_to=info.context.user
                )
                company_data.save()

            data = CompanyData.objects.filter(belongs_to=c_user).get()
            if data.company_picture:
                data.company_picture.storage.delete(data.company_picture.name)
            data.company_picture = file_in
            data.save()
        else:
            if not UserData.objects.filter(belongs_to=info.context.user):
                user_data = UserData(
                    belongs_to=info.context.user
                )
                user_data.save()
            data = UserData.objects.filter(belongs_to=c_user).get()
            if data.profile_picture:
                data.profile_picture.storage.delete(data.profile_picture.name)
            data.profile_picture = file_in
            data.save()

        return UploadUserPicture(ok=True)


class UploadMeisterbrief(graphene.Mutation):
    class Arguments:
        file_in = Upload(required=True, description="Uploaded File")

    ok = graphene.Boolean(description="returns true on successful operation")

    @user_passes_test(lambda u: u.is_company and u.is_authenticated)
    def mutate(self, info, file_in, **kwargs):
        # do something with your file
        c_user = info.context.user
        print(file_in.content_type)

        if file_in.content_type not in ['image/jpg', 'image/jpeg', "image/png", "application/pdf"]:
            raise GraphQLError("Provided invalid file format")

        extension = os.path.splitext(file_in.name)[1]
        file_in.name = "" + str(c_user.pk) + "_meisterbrief" + extension

        data = CompanyData.objects.filter(belongs_to=c_user).get()
        if data.meisterbrief:
            data.meisterbrief.storage.delete(data.meisterbrief.name)
        data.meisterbrief = file_in
        data.save()

        return UploadMeisterbrief(ok=True)


# Create - Update - Delete for all User-Profiles
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdatedProfile.Field()
    update_company = UpdatedCompany.Field()
    delete_user = DeleteUser.Field()
    change_password = ChangePassword.Field()
    change_email = ChangeEmail.Field()
    upload_file = UploadUserPicture.Field()


# Read functions for all Profiles
class Query(graphene.AbstractType):
    me = graphene.Field(UserType, description="returns user model of logged in user")
<<<<<<< HEAD

    # my_company = graphene.Field(CompanyDataType) # not needed, see giant comment below
    # my_user = graphene.Field(UserDataType) # not needed, see giant comment below

=======
    soft_skills = graphene.Field(
        SoftSkillsType,
        description="returns soft skills for logged in User"
    )
>>>>>>> 9e04bc05e92e1de1ba70c9ed02fd64134fd821e4
    # returns auth data
    @login_required  # would return an error on 'Anonymous user', so restricting this to authenticated users
    def resolve_me(self, info):
        return info.context.user

    @user_passes_test(lambda user: not is_company(user))
    def resolve_soft_skills(self, info):
        user = UserData.objects.filter(belongs_to=info.context.user).get()
        return user.soft_skills
        
    # my_company = graphene.Field(CompanyDataType) # not needed, see giant comment below
    # my_user = graphene.Field(UserDataType) # not needed, see giant comment below



'''
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
'''
