from django.contrib import admin

# Register your models here.
from carespace.models import CareSpace, ArticleRead

admin.site.register(CareSpace)
admin.site.register(ArticleRead)
