from django.contrib import admin

from . import models


class ChildInline(admin.TabularInline):
    model = models.Child



admin.site.register(models.Group)
admin.site.register(models.Child)
