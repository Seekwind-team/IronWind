from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator

from django.utils.translation import gettext_lazy as _


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


class Authentication(AbstractUser):

    # Overrides Base User Model
    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[EmailValidator()],
    )
    username = models.CharField(
        _('username'),
        max_length=255,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'


class UserData(models.Model):
    belongs_to = models.ForeignKey(Authentication, on_delete=models.CASCADE)

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class CompanyData(models.Model):
    belongs_to = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE
    )

    description = models.TextField(max_length=500, blank=True)
