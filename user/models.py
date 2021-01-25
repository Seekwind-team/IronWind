from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

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

    # returns model with user data belonging to user
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

    # returns model with badges belonging to current user
    def get_badges(self):
        if not Badges.objects.filter(user=self):
            model = Badges(user=self)
            model.save()
        return Badges.objects.filter(user=self).get()

    def __str__(self):
        # will Return Name of self-objects as stated:
        return "(" + str(self.pk) + ") " + str(self.email)


# saves soft-skill-slider values
class SoftSkills(models.Model):
    # Soft Skills helping Users to find better Job Offers via the implemented Recommender System
    social_activity = models.SmallIntegerField(
        default=0,
        help_text=_("Teamplayer --- Einzelgänger"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    motorskills = models.SmallIntegerField(
        default=0,
        help_text=_("Muskeln --- Fingerspitzengefühl"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    creativity = models.SmallIntegerField(
        default=0,
        help_text=_("Kreativ --- Strikt nach Plan"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    artistic = models.SmallIntegerField(
        default=0,
        help_text=_("Technisch — Gestalterisch"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    customer_orientated = models.SmallIntegerField(
        default=0,
        help_text=_("Hinter den Kulissen --- Kundenorientiert"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    innovativity = models.SmallIntegerField(
        default=0,
        help_text=_("Innovation --- Tradition"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    routine = models.SmallIntegerField(
        default=0,
        help_text=_("Routine --- Abwechslung"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    communicativity = models.SmallIntegerField(
        default=0,
        help_text=_("Stiller Denker --- Kommunikativ"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    planning = models.SmallIntegerField(
        default=0,
        help_text=_("Gleich ran an die Arbeit --- Detaillierte Planung zuerst"),
        validators=[MinValueValidator(limit_value=-6), MaxValueValidator(limit_value=6)],
    )

    def save(self):
        if self.social_activity is None:
            self.social_activity = 0
        if self.motorskills is None:
            self.motorskills = 0
        if self.creativity is None:
            self.creativity = 0
        if self.artistic is None:
            self.artistic = 0
        if self.customer_orientated is None:
            self.customer_orientated = 0
        if self.innovativity is None:
            self.innovativity = 0
        if self.routine is None:
            self.routine = 0
        if self.planning is None:
            self.planning = 0
        if self.communicativity is None:
            self.communicativity = 0
        super(SoftSkills, self).save()


class UserData(models.Model):
    # Data Class representing all additional Data on Non-Company-Users
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

    graduation = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_('what sort of graduation does the user have?')
    )

    graduation_year = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('year of graduation')
    )

    cv = models.JSONField(
        encoder=None,
        null=True,
        blank=True,
        help_text=_('Curriculum Vitae, or CV for short')
    )

    profile_picture = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        help_text=_('profile picture of user')
    )

    def get_profile_picture(self):
        return self.profile_picture.url

    # can't use boolean as we'll define gender as (m/w/d)
    gender = models.TextField(
        max_length=20,
        null=True,
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
        help_text=_('location of user in String (Name of City + ZIP Code)')
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Birth date of user, uses iso8601-Format (eg. 2006-01-02)')
    )

    def __str__(self):
        return "(" + str(self.pk) + "): " + self.belongs_to.email + " User data"


class CompanyData(models.Model):
    # Data Class representing all additional Data on Campany-Users
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
        upload_to='images',
        null=True,
        blank=True,
        help_text=_('eg. Picture of the company Logo')
    )

    meisterbrief = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        help_text=_('Picture to validate the company as legally permitted to accept apprentices')
    )

    def get_company_picture(self):
        return self.company_picture.url

    def __str__(self):
        return "(" + str(self.pk) + "): " + self.belongs_to.email + " company data"


class Note(models.Model):
    # Companies can add notes about users for their convenience
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


class Badges(models.Model):
    """ Badges are represented by their name and an integer-value representing their state and progress,
     usually starting off at 0 and progressing towards a higher number (usually the range will be 0-2 to represent a
     progression in 3 steps) """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_('User Reference'))

    top_vorbereitet = models.IntegerField(
        default=0,
        null=True,
        help_text=_('awarded for reading articles on the app')
    )

    articles_read = models.IntegerField(
        default=0,
        help_text="Number of articles read by user"
    )

    beliebt = models.IntegerField(
        default=0,
        null=True,
        help_text=_('awarded for starting chats')
    )

    chats_started = models.IntegerField(
        default=0,
        null=True,
        help_text=_('number of stats started')
    )

    profil_vollstaendig = models.IntegerField(
        default=0,
        null=True,
        help_text=_('awarded for completing the user profile')
    )

    def __str__(self):
        return "" + str(self.user.__str__()) + "'s Badges"
    

class UserFile(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Description of file uploaded (e.g. \"Lebenslauf\"), 255 chars max."
    )

    file = models.FileField(
        upload_to='static/userfiles/',
        null=True,
        blank=True,
        help_text=_('user files uploaded by user')
    )

    def __str__(self):
        return "(" + str(self.pk) + ") " + ",  \"" + str(self.description) + "\"" + " user: " + str(self.owner.email)


@receiver(pre_delete, sender=UserFile)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


@receiver(pre_delete, sender=UserData)
def img_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.profile_picture.delete(False)


@receiver(pre_delete, sender=CompanyData)
def cimg_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.company_picture.delete(False)
    instance.meisterbrief.delete(False)

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
