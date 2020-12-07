from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CareSpace(models.Model):

    headline = models.CharField(
        null=False,
        max_length=255,
        help_text=_('Headline of this Care-Space Entry')
    )

    header_image = models.ImageField(
        blank=True,
        null=True,
        upload_to='static/carespacecontent/headerimages/',
        help_text=_('Header Image of this Care-Space item')
    )

    body = models.TextField(
        blank=True,
        help_text=_('Body-Text of this Care-Space item')
    )

    author = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Author of this Care-Space item')
    )

    favicon_publisher = models.ImageField(
        blank=True,
        null=True,
        upload_to='static/carespacecontent/icons/',
        help_text=_('Publisher Icon of this Care-Space item')
    )

    publisher = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Publisher of this Care-Space item')
    )

    paid = models.BooleanField(
        default=False,
        help_text=_('Check this box is it is a paid item.')
    )

    rich_text = models.BooleanField(
        default=False,
        help_text=_('Check this box is this is a Rich text item.')
    )

    creation_date = models.DateTimeField(
        default=timezone.now,
        help_text=_('User creation DateTime')
    )

    img_description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Description field for image provided')
    )

    introduction = models.TextField(
        null=True,
        blank=True,
        help_text=_('Short Abstract for this article')
    )

    def __str__(self):
        # will Return Name of self-objects as stated:
        return "ID " + str(self.pk) + ": " + self.headline
