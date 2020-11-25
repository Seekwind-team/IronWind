from django.contrib import admin

# Register your models here.

from .models import Authentication, UserData, CompanyData
admin.site.register(Authentication)
admin.site.register(CompanyData)
admin.site.register(UserData)
