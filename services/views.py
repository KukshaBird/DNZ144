from django.views.generic import TemplateView, ListView

from .models import IssuesModel
from poll.models import Poll

class MainView(TemplateView):
	template_name = 'services/base.html'

class IssuesView(ListView):
	model = IssuesModel
	template_name = 'services/issues.html'

class PollsViewList(ListView):
	model = Poll
	template_name = 'services/polls_list.html'

