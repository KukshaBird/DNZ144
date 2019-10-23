from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
	path('', views.MainView.as_view(), name='services_main'),
	path('issues/', views.IssuesView.as_view(), name='issues'),
	path('closed_issues/', views.ClosedIssuesView.as_view(), name='closed_issues'),
	path('polls/', views.PollsViewList.as_view(), name='polls_list'),
	path('polls/', include(("poll.urls", 'poll_api'), namespace='poll')),
]