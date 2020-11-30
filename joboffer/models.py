from django.db import models
from user.models import Authentication
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import int_list_validator

# used for storing hashtags non-redundant
class Tag(models.Model):
    name = models.CharField(max_length=100, unique = True)


class JobOffer(models.Model):
    owner = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
    )

    hashtags = models.ManyToManyField(
        Tag,
        blank=True
    )

    # job_cats = models.TextField()
    filled = models.BooleanField(
        default=False,
        help_text=_('Definmiert, ob ein Jobangebot besetzt ist')
    )

    is_deleted = models.BooleanField(
        default=False,
        help_text=_('definiert, ob ein Jobangebot "gelöscht" ist')
    )

    #job_cats = models.TextField()
    
    filled = models.BooleanField(default=False)
    
    is_deleted = models.BooleanField(default=False)

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
        blank=True,
        help_text=_('Typ des Jobangebotes, z.B. "Vollzeit"'),
    )

    job_title = models.CharField(
        max_length=255,
        null=True,
        help_text=_('Titel (Name) des Jobangebots')
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Ort des Jobangebots')
    )

    description = models.TextField(
        max_length=4000,
        blank=True,
        null=True,
        help_text=_('Beschreibung des Jobangebots')
    )

    highlights = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=_('Highlights des Jobangebots')
    )
    
    must_have = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=_('Must Haves des Jobangebots (z.B. Führerschein)')
    )
    public_email = models.TextField(
        blank=True,
        null=True,
        help_text=_('Öffentlich sichtbare EMail-Adresse')
    )

    pay_per_year = models.CharField(
        validators=[
            int_list_validator(
                sep=',',
                allow_negative=False)],
        max_length = 100,
        blank = True,
        help_text=_('Lohn pro Ausbildungsjahr')
    )

    pay_per_hour = models.IntegerField(
        blank=True,
        null=True,
        help_text=_('Stundenlohn')
    )

    city = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Ort des Jobangebots')
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        help_text=_('Datum des ersten Arbeitstages')
    )

    trade = models.TextField(
        blank=True,
        null=True,
        help_text=_('Jobkategorie')
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text=_('Erstellungs Datum und Zeit')
    )
    
    last_modified = models.DateTimeField(
        default=timezone.now,
        help_text=_('Zeitpunkt der letzten Änderung')
    )

    def __str__(self):
        return 'Joboffer (' + str(self.id) + ') "' + self.job_title + '"'


# used to store Images for Joboffers
class Image(models.Model):
    name = models.CharField(max_length=255)
    model = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
   
    image = models.ImageField(
        upload_to='images/',
        null=True
    )
   
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)

    def __str__(self):
        return 'Job-ID (' + str(self.model.pk) + ') images'
