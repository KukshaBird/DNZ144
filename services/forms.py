from django.contrib.auth.models import User
from django import forms
from group.models import Group
from .models import IssuesModel
from accounts.models import ApiUser

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'password']

class IssuesCreateForm(forms.ModelForm):

	access_to = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)

	class Meta:
		model = IssuesModel
		fields = ['title', 'description', 'img']
		