from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
	path('', views.MainView.as_view(), name='services_main'),
	path('issues/', views.IssuesView.as_view(), name='issues'),
	path('closed_issues/', views.ClosedIssuesView.as_view(), name='closed_issues'),
	path('issues/details/<pk>', views.DetailIssuesView.as_view(), name='issues_detail'),
	path('issues/create/', views.CreateIssuesView.as_view(), name='issues_create'),
	path('issues/close/<pk>', views.close_issue, name='issues_close'),
	path('issues/create_comment/', views.CreateCommentView.as_view(), name='comment_create'),
	path('kid_polls/', include("kids_poll.urls"), name='kids_poll'),
]