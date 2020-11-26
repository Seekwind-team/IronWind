from django.db import models
from user.models import Authentication
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class JobOffer(models.Model):
    owner = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
    )
    # hashtags = models.TextField()
    # job_cats = models.TextField()
    filled = models.BooleanField(default=False,
                                 help_text=_('Definmiert, ob ein Jobangebot besetzt ist'))
    is_deleted = models.BooleanField(default=False, help_text=_('definiert, ob ein Jobangebot "gelöscht" ist'))

    JOBTYPE_CHOICES = [
        ('Vollzeit', 'Vollzeit'),
        ('Teilzeit', 'Teilzeit'),
        ('Ausbildung', 'Ausbildung'),
        ('Praktikum', 'Praktikum'),
        ('Volunteer', 'Volunteer')
    ]

    job_type = models.CharField(
        max_length=100,
        choices=JOBTYPE_CHOICES,
        default='Vollzeit',
        help_text=_('Typ des Jobangebotes, z.B. "Vollzeit"')
    )

    job_title = models.CharField(
        max_length=255,
        null=True,
        help_text=_('Titel (Name) des Jobangebots')
    )

    # Hier sollte sich überlegt werden, wie mit Geo-Locations umgegangen wird
    location = models.CharField(
        max_length=100,
        null=True,
        help_text=_('Ort des Jobangebots')
    )

    description = models.TextField(
        max_length=4000,
        null=True,
        help_text=_('Beschreibung des Jobangebots')
    )

    highlights = models.TextField(
        max_length=1000,
        null=True,
        help_text=_('Highlights des Jobangebots')
    )
    must_have = models.TextField(
        max_length=1000,
        null=True,
        help_text=_('Must Haves des Jobangebots (z.B. Führerschein)')
    )

    public_email = models.EmailField(
        null=True,
        help_text=_('Öffentlich sichtbare EMail-Adresse')
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text=_('Erstellungs Datum und Zeit')
    )
    last_modified = models.DateTimeField(
        default=timezone.now,
        help_text=_('Zeitpunkt der letzten Änderung')
    )


# used to store Images for Joboffers
class Image(models.Model):
    name = models.CharField(max_length=255)
    model = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)
