from django.contrib import admin

from . import models


@admin.register(models.ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
    pass
