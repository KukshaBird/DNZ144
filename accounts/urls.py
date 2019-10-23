from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
	path('', views.SignUp.as_view(), name='signup'),
	path('details/<pk>', views.AccountDetailView.as_view(), name='account_detail'),
	path('logout', views.logout_view, name='logout'),
	# path('login', views.login_view, name='login'),
	path('login', views.UserLoginView.as_view(), name='login'),
]