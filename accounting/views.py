from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Kassa, Operation
from group.models import Group, Kid
from accounts.models import ApiUser
from django.db.models import Sum

#forms
from .forms import CreateOperationForm, CreateWithdrawForm, CreateTransferForm

# Create your views here.

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
		#TODO: create list of groups.
		queryset = (Group.objects.
			get(pk=self.request.user.get_group_list()[0].pk).
			kassas.filter(is_active=True).
			order_by('-create_date'))
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		total_sum = sum([kassa.get_saldo() for kassa in Group.objects.get(pk=self.request.user.get_group_list()[0].pk).kassas.all()]) if self.request.user.get_group_list() else "Нет доступа к группам"
		context['total_sum'] = total_sum
		return context

class KassaDetailView(LoginRequiredMixin, DetailView):
	model = Kassa
	template_name = 'kassas_details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['kid_balance'] = context['kassa'].kid_balance(self.request.user.kids.first())['balance']
		return context

#Create Operation
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


def withdraw_submit(request):
	response_data = {}
	form = CreateWithdrawForm(request.POST)
	if form.is_valid():
		form = form.cleaned_data
		kassa = form['from_kassa']
		kassa.withdraw(form['amount'], ApiUser.objects.get(id=request.user.id))
		return JsonResponse(response_data)

def transfer_submit(request):
	response_data = {}
	if request.is_ajax:
		responsible_user = ApiUser.objects.get(id=request.user.id)
		form = CreateTransferForm(request.POST)
		if form.is_valid():
			form = form.cleaned_data
			from_k = form['from_kassa']
			to_k = form['to_kassa']
			if from_k and to_k:
				rest = from_k.get_saldo()
				if rest > 0:
					committed = from_k.kids_paid()
					for kid_id in committed:
						kid_obj = Kid.objects.get(id=kid_id)
						# kid_deb = from_k.kid_balance(kid_obj)['deb']
						kid_balance = from_k.kid_balance(kid_obj)['balance']
						# kid_quota = kid_deb / from_k.get_deb_sum()
						# trans = round(rest * kid_quota, 2)
						trans = round(kid_balance, 2)
						if trans != 0:
							from_k.operations.create(
									kassa=from_k,
									kid=kid_obj,
									amount=trans,
									user = responsible_user,
									trans_type = "CRE"
								)
							to_k.operations.create(
									kassa=to_k,
									kid=kid_obj,
									amount=trans,
									user = responsible_user,
									trans_type = "DEB"
								)
					return JsonResponse(response_data)
				elif rest < 0:
					for kid_obj in from_k.group.kids.all():
						# kid_deb = from_k.kid_balance(kid_obj)['deb']
						# kid_balance = from_k.kid_balance(kid_obj)['balance']
						trans = abs(round(rest / len(from_k.group.kids.all()), 2))
						if trans != 0:
							from_k.operations.create(
									kassa=from_k,
									kid=kid_obj,
									amount=trans,
									user = responsible_user,
									trans_type = "DEB"
								)
							to_k.operations.create(
									kassa=to_k,
									kid=kid_obj,
									amount=trans,
									user = responsible_user,
									trans_type = "CRE"
								)
					return JsonResponse(response_data)
		else:
			form = CreateTransferForm()
			return JsonResponse(response_data)

def operation_submit(request):
	response_data = {}
	if request.is_ajax:
		if request.method == 'POST':
			data = request.POST
			if data['trans_type'] == "DEB":
				Operation.objects.get_or_create(
					kassa=Kassa.objects.get(pk=data['kassa']),
					kid=Kid.objects.get(pk=data['kid']),
					amount=data['amount'],
					user = ApiUser.objects.get(id=request.user.id),
					trans_type = data['trans_type'])
			if data['trans_type'] == "CRE":
				Operation.objects.get_or_create(
					kassa=Kassa.objects.get(pk=data['kassa']),
					amount=data['amount'],
					user = ApiUser.objects.get(id=request.user.id),
					trans_type = data['trans_type'])
			return JsonResponse(response_data)



