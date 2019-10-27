from django.views.generic import (TemplateView, ListView,
									DetailView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import IssuesModel, Comment
from poll.models import Poll
from group.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

from .forms import IssuesCreateForm

class MainView(TemplateView):
	template_name = 'services/base.html'

class IssuesView(ListView):
	model = IssuesModel
	template_name = 'services/issues.html'

	def get_queryset(self):
		if self.request.user.is_authenticated:
			queryset = IssuesModel.objects.filter(
					access_to__in=self.request.user.get_group_list()
				).filter(is_closed__exact=False)
			return queryset
		else:
			return False

class ClosedIssuesView(ListView):
	model = IssuesModel
	template_name = 'services/closed_issues.html'

	def get_queryset(self):
		if self.request.user.is_authenticated:
			queryset = IssuesModel.objects.filter(
					access_to__kids__parents__exact=User.objects.get(
						id=self.request.user.id
					)
				).filter(is_closed__exact=True)
			return queryset
		else:
			return False

class DetailIssuesView(DetailView):
	model = IssuesModel
	template_name = 'services/issues_detail.html'

class CreateIssuesView(LoginRequiredMixin, CreateView):
	model = IssuesModel
	form_class = IssuesCreateForm
	template_name = 'services/issues_create.html'
	success_url = reverse_lazy('services:issues')

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.save()
		form.instance.access_to.set(self.request.POST.get("access_to"))
		return super().form_valid(form)

class CreateCommentView(LoginRequiredMixin, CreateView):
	model = Comment
	template_name = 'services/issues_create.html'
	fields = '__all__'
	success_url = reverse_lazy('services:issues')

class PollsViewList(ListView):
	model = Poll
	template_name = 'services/polls_list.html'

	def get_queryset(self):
		if self.request.user.is_authenticated:
			queryset = Poll.objects.filter(group_polls__exact=self.request.user.get_group_list()[0].id)
			return queryset
		else:
			return False

class CreatePollView(LoginRequiredMixin, CreateView):
	model = Poll
	template_name = 'poll/polls_create.html'
	fields = ['question']
	success_url = reverse_lazy('services:polls_list')