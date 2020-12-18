from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from IronWind import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class Authentication(AbstractBaseUser, PermissionsMixin):
    # Overrides Base User Model
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('email address used for authentication'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractBaseUser.Meta):
        abstract = False
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        swappable = 'AUTH_USER_MODEL'

    # custom User-Fields
    is_company = models.BooleanField(
        default=False,
        help_text=_('defines whether the account used is a company account or a user account'),
    )

    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
        help_text=_('User creation DateTime')
    )

    def get_data(self):
        if self.is_company:
            if not CompanyData.objects.filter(belongs_to=self):
                company_data = CompanyData(
                    belongs_to=self
                )
                company_data.save()
            return CompanyData.objects.filter(belongs_to=self).get()
        else:
            if not UserData.objects.filter(belongs_to=self):
                user_data = UserData(
                    belongs_to=self
                )
                user_data.save()
            return UserData.objects.filter(belongs_to=self).get()

    def __str__(self):
        # will Return Name of self-objects as stated:
        return "(" + str(self.pk) + ") " + str(self.email)

# saves soft-skill-slider 
class SoftSkills(models.Model):
    social_activity=models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(limit_value=-5), MaxValueValidator(limit_value=5)],
        help_text=_("Teamplayer --- Einzelgänger"),
        #copy paste
    )

    motorskills=models.SmallIntegerField(
        default=0,
        help_text=_("Muskeln --- Fingerspitzengefühl"),
        #copy paste
    )

    creativity=models.SmallIntegerField(
        default=0,
        help_text=_("Kreativ --- Strikt nach Plan"),
        #copy paste
    )

    artistic=models.SmallIntegerField(
        default=0,
        help_text=_("Technisch — Gestalterisch"),
        #copy paste
    )

    customer_orientated=models.SmallIntegerField(
        default=0,
        help_text=_("Hinter den Kulissen --- Kundenorientiert"),
        #copy paste
    )

    innovativity=models.SmallIntegerField(
        default=0,
        help_text=_("Innovation --- Tradition"),
        #copy paste
    )

    routine=models.SmallIntegerField(
        default=0,
        help_text=_("Routine --- Abwechslung"),
        #copy paste
    )

    communicativity=models.SmallIntegerField(
        default=0,
        help_text=_("Stiller Denker --- Kommunikativ"),
        #copy paste
    )

    planning=models.SmallIntegerField(
        default=0,
        help_text=_("Gleich ran an die Arbeit --- Detaillierte Planung zuerst"),
        #copy paste
    )


class UserData(models.Model):
    belongs_to = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text=_('User Reference'))

    first_name = models.CharField(
        _('first name'),
        max_length=150,
        null=True,
        blank=True,
        help_text=_('First name of User')
    )

    last_name = models.CharField(
        _('last name'),
        max_length=150,
        null=True,
        blank=True,
        help_text=_('Last name of User')
    )

    phone_number = models.CharField(
        _('phone number'),
        max_length=21,
        null=True,
        blank=True,
        help_text=_('Telephone number of user, uses E.165-Format')
    )

    short_bio = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        help_text=_('Short self-description of user, 2000 characters maximum')
    )

    looking = models.BooleanField(
        default=True,
        help_text=_('Is actively looking for Job Offers?')
    )

    # TODO: Grades ?
    # TODO: Graduation ?

    profile_picture = models.ImageField(
        upload_to='static/images/',
        null=True,
        blank=True,
        help_text=_('profile picture of user')
    )

    def get_profile_picture(self):
        return self.profile_picture.url

    # can't use boolean as we'll define gender as (m/w/d)
    gender = models.TextField(
        max_length=20,
        blank=True,
        help_text=_('gender of User, uses string to allow all genders')
    )

    # TODO: Geo-Locations?

    # soft skills slider values
    soft_skills = models.OneToOneField(
        SoftSkills,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_('Reference to slider values for soft skills')
    )

    location = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_('location of user in String (eg. Name of City)')
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Birth date of user, uses iso8601-Format (eg. 2006-01-02)')
    )

    def delete(self, using=None, keep_parents=False):
        self.profile_picture.storage.delete(self.profile_picture.name)
        super().delete()

    def __str__(self):
        return "(" + str(self.pk) + "): " + self.belongs_to.email + " User data"


class CompanyData(models.Model):
    belongs_to = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_('User Reference')
    )

    company_name = models.TextField(
        max_length=255,
        null=False,
        help_text=_('name of company')
    )

    description = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        help_text=_('short description of the company, 2000 characters maximum')
    )

    first_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text=_('Fist name of the responsible HR manager')
    )

    last_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text=_('last name of the responsible HR Manager')
    )

    # TODO: Geo-Location ?

    phone_number = models.CharField(
        _('phone number'),
        max_length=21,
        null=True,
        blank=True,
        help_text=_('Phone number of the company, uses E.165-Format')
    )

    company_picture = models.ImageField(
        upload_to='static/images/',
        null=True,
        blank=True,
        help_text=_('eg. Picture of the company Logo')
    )

    meisterbrief = models.ImageField(
        upload_to='static/images/',
        null=True,
        blank=True,
        help_text=_('Picture to validate the company as legally permitted to accept apprentices')
    )

    def get_company_picture(self):
        return self.company_picture.url

    def delete(self, using=None, keep_parents=False):
        self.company_picture.storage.delete(self.song.name)
        self.meisterbrief.storage.delete(self.song.name)
        super().delete()

    def __str__(self):
        return "(" + str(self.pk) + "): " + self.belongs_to.email + " company data"


class Notizfeld(models.Model):

    user_from = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
        related_name='%(class)s_sender',
    )

    user_to = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
        related_name='%(class)s_receiver',
    )

    memo = models.TextField(
        _('memo field'),
        null=True,
        blank=True,
        max_length=5000,
        help_text=_('Memo field to leave a note on an applicant')
    )


'''
# class Image(models.Model):
    """ProfileImage"""
    user = models.ForeignKey(Authentication, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profileimages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return profile image"""
        return self.image.url
'''
