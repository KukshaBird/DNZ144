from django.contrib import admin

from . import models

class OperationAdmin(admin.ModelAdmin):
    list_display = ['create_date', 'kid', 'trans_type', 'kassa', 'amount']
    list_filter = ['kid', 'trans_type', 'kassa']

admin.site.register(models.Kassa)
admin.site.register(models.Operation, OperationAdmin)
