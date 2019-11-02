from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


# from group import models as group_model

@admin.register(models.ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
	pass


# admin.site.register(models.Profile)
