from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import Authentication


class Message(models.Model):
    sender = models.OneToOneField(
        Authentication,
        on_delete=models.CASCADE,
        related_name='%(class)s_sender',
        help_text=_('sender')
    )
    receiver = models.OneToOneField(
        Authentication,
        on_delete=models.CASCADE,
        related_name='%(class)s_receiver',
        help_text=_('receiver')
    )

    message = models.CharField(
        null=False,
        blank=False,
        max_length=1999,
        help_text=_('Headline of this Care-Space Entry')
    )

    timestamp = models.DateTimeField(default=timezone.now)


