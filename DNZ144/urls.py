"""DNZ144 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls'), name='django_auth'),
    path('', views.home_view, name='home'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('info/', views.info_view, name='info'),
    path('info/staff', views.staff_view, name='staff'),
    path('info/schedule', views.schedule_view, name='schedule'),
    path('services/', include('services.urls'), name='services'),
    path('groups/', include('group.urls'), name='group'),
    path('registration/', include('accounts.urls'), name='registration'),
    path('accounting/', include('accounting.urls'), name='accounting'),
]
