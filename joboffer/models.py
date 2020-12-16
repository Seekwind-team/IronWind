from django.db import models
from user.models import Authentication, UserData
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import int_list_validator


# used for storing hashtags non-redundant
class Tag(models.Model):
    name = models.CharField(max_length=100, unique = True)
    def __str__(self):
        return str(self.name)


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
        help_text=_('Titel (Name) des Jobangebots')
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Ort des Jobangebots')
    )

    description = models.TextField(
        max_length=8000,
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

    nice_have = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=_('Nice to Haves des Jobangebots (z.B. beherscht Englisch)')
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
                allow_negative=False
            )
        ],
        max_length = 100,
        blank = True,
        null = True,
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

    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()
        super(JobOffer, self).save(*args, **kwargs)


# used to store Images for Joboffers
class Image(models.Model):
    model = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        help_text=_('Job this Image belongs to')
    )
   
    image = models.ImageField(
        upload_to='static/jobImages/',
        null=False,
        help_text=_('Imagefile with metadata')
    )

    description = models.CharField(max_length=255, null=True, blank=True, help_text=_('Description of Image, 255 char max'))
   
    default = models.BooleanField(default=False, help_text=_('is this the default image?'))
    width = models.FloatField(default=0, help_text=_('width of this image, will be set automatically on upload'))
    height = models.FloatField(default=0, help_text=_('height of this image, will be set automatically on upload'))

    def __str__(self):
        return self.image.url


# used to store like or dislike from user on joboffer
class Swipe(models.Model):
    candidate = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE
    )

    job_offer = models.ForeignKey(
        JobOffer, 
        on_delete=models.CASCADE
    )

    liked = models.BooleanField(
        blank=False,
    )


# used to store joboffer for user as bookmarks
class Bookmark(models.Model):
    candidate = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE
    )

    job_offer = models.ForeignKey(
        JobOffer, 
        on_delete=models.CASCADE
    )