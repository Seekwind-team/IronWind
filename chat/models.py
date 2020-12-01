from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import Authentication


class Chatroom(models.Model):
    participants = ArrayField(
            models.ForeignKey(
                Authentication,
                on_delete=models.CASCADE
            ),
            size=2
    )


class Message(models.Model):
    sender = models.OneToOneField(
        Authentication,
        related_name='%(class)s_sender',
        on_delete=models.CASCADE
    )
    receiver = models.OneToOneField(
        Authentication,
        on_delete=models.CASCADE,
        related_name='%(class)s_receiver'
    )

    message = models.CharField(
        null=False,
        blank=False,
        max_length=1999,
        help_text=_('Headline of this Care-Space Entry')
    )

    chatroom = models.OneToOneField(Chatroom, on_delete=models.CASCADE)


