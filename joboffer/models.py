from django.db import models
from user.models import Authentication
from django.utils import timezone


class JobOffer(models.Model):
    owner = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
    )
    # hashtags = models.TextField()
    # job_cats = models.TextField()
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
        default='Vollzeit'
    )

    job_title = models.CharField(
        max_length=255,
        null=True
    )

    # Hier sollte sich überlegt werden, wie mit Geo-Locations umgegangen wird
    location = models.CharField(
        max_length=100,
        null=True
    )

    description = models.TextField(
        max_length=4000,
        null=True
    )

    highlights = models.TextField(
        max_length=1000,
        null=True
    )
    must_have = models.TextField(
        max_length=1000,
        null=True
    )
    public_email = models.EmailField(
    )
    company_logo = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(
        default=timezone.now
    )
    last_modified = models.DateTimeField(
        default=timezone.now
    )


# used to store Images for Joboffers
class Image(models.Model):
    name = models.CharField(max_length=255)
    model = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)
