from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Kassa
from group.models import Group

# Create your views here.

@login_required
def test_view(request):
	kassa = Kassa.objects.all()[0]
	return render(request, 'accounting/accounting_base.html', context={'kassa': kassa})
