from django.contrib import admin

from . import models


class KidInline(admin.TabularInline):
    model = models.Kid



admin.site.register(models.Group)
admin.site.register(models.Kid)
admin.site.register(models.Staff)
