from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView)
from django.urls import reverse_lazy

from .models import Poll, Item, Vote

from .forms import CreatePollForm


def vote(request, poll_id):
    if request.is_ajax():

        try:
            poll = Poll.objects.get(pk=poll_id)
        except Poll.DoesNotExist:
            return HttpResponse('Wrong parameters', status=400)

        item_id = request.GET.get("item", False)

        if not item_id:
            return HttpResponse('Wrong parameters', status=400)

        try:
            item = Item.objects.get(pk=item_id)
        except:
            return HttpResponse('Wrong parameters', status=400)

        Vote.objects.create(
            poll=poll,
            ip=request.META['REMOTE_ADDR'],
            item=item,
            kid=request.user.kids.first(),
        )
        response = HttpResponse(status=200)

        return response
    return HttpResponse(status=400)


def poll_view(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except:
        return HttpResponse('Wrong parameters', status=400)

    try:
        items = Item.objects.filter(poll=poll)
    except:
        return HttpResponse('Wrong parameters', status=400)

    context = {'poll': poll, 'items': items,}

    #if user have not group yet
    if len(request.user.get_group_list()) < 1:
        return render(request, "result.html", context)

    # if user's kid have voted render results
    users_kid = request.user.kids.first()
    if Vote.objects.filter(poll=poll,kid=users_kid).exists():
        return render(request, "result.html", context)
    else:
        return render(request, "poll.html", context)  
    
def result(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except:
        return HttpResponse('Wrong parameters', status=400)

    try:
        items = Item.objects.filter(poll=poll)
    except:
        return HttpResponse('Wrong parameters', status=400)

    context = {'poll': poll,'items': items,}

    return render(request, "result.html", context)


def percentage(poll, item):
    poll_vote_count = poll.get_vote_count()
    if poll_vote_count > 0:
        return float(item.get_vote_count()) / float(poll_vote_count) * 100

class PollsViewList(LoginRequiredMixin, ListView):
    model = Poll
    template_name = 'polls_list.html'

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         queryset = Poll.objects.filter(groups__id=self.request.user.get_group_list()[0].id)
    #         return queryset
    #     else:
    #         return False

class CreatePollView(LoginRequiredMixin, CreateView):
    # model = Poll
    form_class = CreatePollForm
    template_name = 'polls_create.html'
    # fields = '__all__'
    success_url = reverse_lazy('services:kids_poll:polls_list')

    def form_valid(self, form):
        super().form_valid(form)
        cleaned_form = form.cleaned_data
        for k, v in cleaned_form.items():
            if 'answer' in k and v != "":
                Item.objects.create(
                    value = v,
                    poll = Poll.objects.last()
                    )
        return super().form_valid(form)