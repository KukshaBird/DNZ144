from django.shortcuts import render

def home_view(request):
	return render(request, 'home.html')

def contacts_view(request):
	return render(request, 'contacts.html')

def info_view(request):
	return render(request, 'info.html')

def schedule_view(request):
	return render(request, 'info/schedule.html')

def staff_view(request):
	return render(request, 'info/staff.html')