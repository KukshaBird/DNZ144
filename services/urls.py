from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
	path('', views.MainView.as_view(), name='services_main'),
	path('issues/', views.IssuesView.as_view(), name='issues'),
	path('closed_issues/', views.ClosedIssuesView.as_view(), name='closed_issues'),
	path('issues/details/<pk>', views.DetailIssuesView.as_view(), name='issues_detail'),
	path('issues/create/', views.CreateIssuesView.as_view(), name='issues_create'),
	path('issues/create_comment/', views.CreateCommentView.as_view(), name='comment_create'),
	path('polls/', views.PollsViewList.as_view(), name='polls_list'),
	path('polls/create', views.CreatePollView.as_view(), name='polls_create'),
	path('polls/', include(("poll.urls", 'poll_api'), namespace='poll')),
]