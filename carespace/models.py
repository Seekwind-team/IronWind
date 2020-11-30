from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CareSpace(models.Model):

    headline = models.CharField(
        null=False,
        max_length=255,
        help_text=_('Headline of Care-Space Entry')
    )

    header_image = models.ImageField(
        upload_to='static/carespacecontent/headerimages/',
        help_text=_('Header Image of Care-Space item')
    )

    body = models.TextField(
        null=True,
        blank=True,
        help_text=_('Body-Text of Care-Space item')
    )

    author = models.TextField(
        null=True,
        blank=False,
        help_text=_('Author of Care-Space item')
    )

    favicon_publisher = models.ImageField(
        upload_to='static/carespacecontent/icons/',
        help_text=_('Publisher Icon of Care-Space item')
    )

    publisher = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Publisher Care-Space item')
    )

    paid = models.BooleanField(
        default=False,
        help_text=_('is this paid item?')
    )

    rich_text = models.BooleanField(
        default=False,
        help_text=_('Rich text item?')
    )

    creation_date = models.DateTimeField(
        default=timezone.now,
        help_text=_('User creation DateTime')
    )
