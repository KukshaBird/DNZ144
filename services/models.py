from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class IssuesModel(models.Model):
	name = models.CharField(max_length=155)
	description = models.TextField()
	is_closed = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class UserForm(ModelForm):

	class Meta:
		model = User
		fields = ['username', 'password']
		