from django import forms
from .models import Poll

class CreatePollForm(forms.ModelForm):

	answer1 = forms.CharField(max_length=255, required=False)
	answer2 = forms.CharField(max_length=255, required=False)
	answer3 = forms.CharField(max_length=255, required=False)

	class Meta:
		model = Poll
		fields = ['question']