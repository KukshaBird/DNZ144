from django.contrib import admin
from . import models

admin.site.register(models.IssuesModel)
admin.site.register(models.Comment)
admin.site.register(models.IssuePoll)
