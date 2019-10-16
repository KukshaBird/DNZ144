from django.db import models

class IssuesModel(models.Model):
	name = models.CharField(max_length=155)
	description = models.TextField()
	is_closed = models.BooleanField(default=False)

	def __str__(self):
		return self.name
