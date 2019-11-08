from django.views.generic import (TemplateView, ListView,
									DetailView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import IssuesModel, Comment
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
	fields = ['text']
	success_url = reverse_lazy('services:issues')

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.issue = IssuesModel.objects.get(pk=self.kwargs['pk'])
		form.instance.save()
		return super().form_valid(form)

@login_required
def close_issue(request, pk):
	issue = get_object_or_404(IssuesModel, pk=pk)
	issue.close_issue()
	return redirect('services:issues')
