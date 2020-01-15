from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django.http import JsonResponse

from .models import Kassa, Operation
from group.models import Group
from accounts.models import ApiUser
from django.db.models import Sum

# forms
from .forms import CreateOperationForm, CreateWithdrawForm, CreateTransferForm

# functions for kassa's operations
from .utils import *


@login_required
def test_view(request):
    kassa = Kassa.objects.all()[1]
    return render(request, 'accounting/accounting_base.html', context={'kassa': kassa})


from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class KassaListView(LoginRequiredMixin, ListView):
    model = Kassa
    # get_context_object_name = 'kassas'
    template_name = 'kassas_list.html'
    redirect_field_name = 'accounts:login'

    def get_queryset(self):
        if not self.request.user.has_group():
            return None
        # TODO: create list of groups.
        queryset = (Group.objects.
                    get(pk=self.request.user.get_group_list()[0].pk).
                    kassas.filter(is_active=True, is_charity=False).
                    order_by('-create_date'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_sum = sum([kassa.get_saldo() for kassa in Group.objects.get(pk=self.request.user.get_group_list()[
            0].pk).kassas.all()]) if self.request.user.get_group_list() else "Нет доступа к группам"
        context['total_sum'] = total_sum
        return context


class KassaClosedListView(LoginRequiredMixin, ListView):
    model = Kassa
    # get_context_object_name = 'kassas'
    template_name = 'kassas_closed_list.html'
    redirect_field_name = 'accounts:login'

    def get_queryset(self):
        if not self.request.user.has_group():
            return None
        # TODO: create list of groups.
        queryset = (Group.objects.
                    get(pk=self.request.user.get_group_list()[0].pk).
                    kassas.filter(is_active=False).
                    order_by('-create_date'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_sum = sum([kassa.get_saldo() for kassa in Group.objects.get(pk=self.request.user.get_group_list()[
            0].pk).kassas.all()]) if self.request.user.get_group_list() else "Нет доступа к группам"
        context['total_sum'] = total_sum
        return context


class KassaCharityListView(LoginRequiredMixin, ListView):
    model = Kassa
    template_name = 'kassas_charity_list.html'
    redirect_field_name = 'accounts:login'

    def get_queryset(self):
        if not self.request.user.has_group():
            return None
        # TODO: create list of groups.
        queryset = (Group.objects.
                    get(pk=self.request.user.get_group_list()[0].pk).
                    kassas.filter(is_active=True, is_charity=True).
                    order_by('-create_date'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_sum = sum([kassa.get_saldo() for kassa in Group.objects.get(pk=self.request.user.get_group_list()[
            0].pk).kassas.all()]) if self.request.user.get_group_list() else "Нет доступа к группам"
        context['total_sum'] = total_sum
        return context


class KassaDetailView(LoginRequiredMixin, DetailView):
    model = Kassa
    template_name = 'kassas_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kid_balance'] = context['kassa'].kid_balance(self.request.user.kids.first())['balance']
        return context


# Create Operation
@login_required
def create_operation(request):
    form = CreateOperationForm
    return render(request, 'create_operation.html', context={'form': form})


@login_required
def create_withdraw(request):
    form = CreateWithdrawForm
    return render(request, 'create_withdraw.html', context={'form': form})


@login_required
def create_transfer(request):
    form = CreateTransferForm
    return render(request, 'create_transfer.html', context={'form': form})


@require_http_methods(["POST"])
def withdraw_submit(request):
    response_data = {}
    form = CreateWithdrawForm(request.POST)
    if form.is_valid():
        form = form.cleaned_data
        kassa = form['from_kassa']
        withdraw(kassa, form['amount'], user=ApiUser.objects.get(id=request.user.id))
        # kassa.withdraw(form['amount'], ApiUser.objects.get(id=request.user.id))
        return JsonResponse(response_data)


@require_http_methods(["POST"])
def transfer_submit(request):
    """
	if not amount provide:
	function transfer all kassa's balance to another kassa. End part amount for each Kid dependent from their donate.
		If balance is negative, function draws amount from another kassa equly from each kid. Anyway, from_k's balance
		will set to zero.
	else: transfer provided amount.
	:param request: POST from FORM.
    :return: empty dictionary object.
	"""
    response_data = {}
    if request.is_ajax:
        responsible_user = ApiUser.objects.get(id=request.user.id)
        form = CreateTransferForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            from_k = form['from_kassa']
            to_k = form['to_kassa']
            amount = form['amount']
            if from_k and to_k:
                trans_func(from_k, to_k, responsible_user, amount)
            return JsonResponse(response_data)
        else:
            return JsonResponse(response_data)


@require_http_methods(["POST"])
def operation_submit(request):
    response_data = {}
    if request.is_ajax:
        if request.method == 'POST':
            data = request.POST
            Operation.objects.get_or_create(
                kassa=Kassa.objects.get(pk=data['kassa']),
                kid=Kid.objects.get(pk=data['kid']),
                amount=data['amount'],
                user=ApiUser.objects.get(id=request.user.id),
                trans_type=data['trans_type'],
                comment=data['comment']
            )
            return JsonResponse(response_data)
