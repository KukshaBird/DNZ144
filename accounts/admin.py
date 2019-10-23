from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


from group import models as group_model

admin.site.register(models.Profile)
admin.site.register(models.ApiUser, UserAdmin)
