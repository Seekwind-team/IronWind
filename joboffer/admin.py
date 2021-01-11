from django.contrib import admin

# Register your models here.

from .models import JobOffer, Image, Swipe

admin.site.register(JobOffer)
admin.site.register(Image)
admin.site.register(Swipe)
