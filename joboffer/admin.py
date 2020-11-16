from django.contrib import admin

# Register your models here.

from .models import JobOffer, Image
admin.site.register(JobOffer, Image)