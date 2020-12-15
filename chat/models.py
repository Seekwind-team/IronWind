from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import Authentication


class Message(models.Model):
    sender = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
        unique=False,
        related_name='%(class)s_sender',
        help_text=_('sender')
    )
    receiver = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
        unique=False,
        related_name='%(class)s_receiver',
        help_text=_('receiver')
    )

    message = models.CharField(
        null=False,
        blank=False,
        unique=False,
        max_length=255,
        help_text=_('message sent through chat message')
    )

    unread = models.BooleanField(
        default=True,
        help_text=_('Whether this message has been read or not')
    )

    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # will Return Name of self-objects as stated:
        return str(self.sender.email) + " (at " + str(self.timestamp) + "): " + str(self.message)


