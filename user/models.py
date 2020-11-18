from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

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
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractBaseUser.Meta):
        abstract = False
        verbose_name = _('Nutzer')
        verbose_name_plural = _('Nutzer')
        swappable = 'AUTH_USER_MODEL'

    # custom User-Fields
    is_company = models.BooleanField(
        default=False
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


class UserData(models.Model):
    belongs_to = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    phone_number = models.CharField(_('phone number'),max_length=21, blank=True)

    short_bio = models.TextField(max_length=500, blank=True)

    # TODO: Grades ?
    # TODO: Graduation ?

    profile_picture = models.ImageField(upload_to='images/')
    # can't use boolean as we'll define gender as (m/w/d)
    gender = models.TextField(max_length=20)

    # TODO: Soft Skills?
    # TODO: Geo-Locations?

    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class CompanyData(models.Model):
    belongs_to = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    company_name = models.TextField(max_length=255)
    description = models.TextField(max_length=2000, blank=True)

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    # TODO: Geo-Location ?

    phone_number = models.CharField(_('phone number'), max_length=21, blank=True)
    company_picture = models.ImageField(upload_to='images/')
    meisterbrief = models.ImageField(upload_to='images/')

