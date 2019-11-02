from django import forms
from .models import Operation, Kassa

class CreateOperationForm(forms.ModelForm):

	class Meta:
		model = Operation
		fields = ['trans_type', 'kassa', 'kid', 'amount']

class CreateTransferForm(forms.Form):
	from_kassa = forms.ModelChoiceField(queryset=Kassa.objects.all(), empty_label=None)
	to_kassa = forms.ModelChoiceField(queryset=Kassa.objects.all(), empty_label=None)
	# amount = forms.DecimalField(max_digits=7, decimal_places=2)

class CreateWithdrawForm(forms.Form):
	from_kassa = forms.ModelChoiceField(queryset=Kassa.objects.all(), empty_label=None)
	amount = forms.DecimalField(max_digits=7, decimal_places=2)



		