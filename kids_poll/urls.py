from django.urls import path
from . import views

app_name = 'kids_poll'

urlpatterns = [
	path('votes/<poll_id>', views.vote, name='vote'),
	path('polls/<poll_id>', views.poll_view, name='poll_view'),
	path('result/<poll_id>', views.result, name='result'),
	path('polls/', views.PollsViewList.as_view(), name='polls_list'),
	path('polls/create/', views.CreatePollView.as_view(), name='polls_create'),
]