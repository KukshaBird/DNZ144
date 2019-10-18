from django.contrib import admin

from . import models


from group import models as group_model


class ChildInline(admin.TabularInline):
    model = group_model.Child

admin.site.register(models.Group)
admin.site.register(models.Kid)
admin.site.register(models.Parent)
admin.site.register(models.Family)