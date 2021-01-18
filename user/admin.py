from django.contrib import admin

# Register your models here.

from .models import Authentication, UserData, CompanyData, UserFile, Badges
admin.site.register(Authentication)
admin.site.register(CompanyData)
admin.site.register(UserData)
admin.site.register(UserFile)
admin.site.register(Badges)
