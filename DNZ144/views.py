from django.shortcuts import render
from django.conf import settings
import os

from group.models import Staff

def home_view(request):
	with open(os.path.join(settings.BASE_DIR, 'welcome.txt'),
				mode='r',
				encoding="utf-8") as f:
		text = f.read()

	return render(request, 'home.html', context={'text': text})

def contacts_view(request):
	return render(request, 'contacts.html')

def info_view(request):
	return render(request, 'info.html')

def schedule_view(request):
	return render(request, 'info/schedule.html')

def staff_view(request):
	staff_list = Staff.objects.all()
	return render(request, 'info/staff.html',context={'staff_list': staff_list})