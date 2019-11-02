from django.db import models
from django.db.models import Sum

from accounts.models import ApiUser
from group.models import Group, Kid


class Kassa(models.Model):
	name = models.CharField(max_length=32)
	card = models.CharField(max_length=16, null=True, blank=True)
	group = models.ForeignKey(Group, related_name='kassas',
								on_delete=models.CASCADE, null=True)
	create_date = models.DateField(auto_now_add=True, null=True)
	descripton = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return "details/%i" % self.id

	def get_cre_sum(self):
		return self.operations.filter(trans_type="CRE").aggregate(Sum('amount'))['amount__sum']

	def get_deb_sum(self):
		return self.operations.filter(trans_type="DEB").aggregate(Sum('amount'))['amount__sum']

	def get_saldo(self):
		# cre = self.get_cre_sum()
		# deb = self.get_deb_sum()
		cre = self.operations.filter(trans_type="CRE").aggregate(Sum('amount'))['amount__sum']
		deb = self.operations.filter(trans_type="DEB").aggregate(Sum('amount'))['amount__sum']
		if deb and cre: return deb - cre
		elif deb: return deb
		else: return 0

	def withdraw(self, amount, user):
		# withdraw from each kid balance
		kids_list = self.group.kids.all()
		avg_sum = round(amount / len(kids_list), 2)
		for kid in kids_list:
			self.operations.create(
					kid = kid,
					kassa = self,
					amount = avg_sum,
					trans_type = 'CRE',
					user = user,
				)
		return True

	def kids_paid(self):
		kids_paid = [kid[0] for kid in self.operations.filter(trans_type="DEB").values_list('kid')]
		return kids_paid

	def kid_balance(self, kid):
		cre = self.operations.filter(trans_type="CRE", kid=kid).aggregate(Sum('amount'))['amount__sum']
		deb = self.operations.filter(trans_type="DEB",kid=kid).aggregate(Sum('amount'))['amount__sum']
		if deb and cre:
			return {'cre': cre, 'deb': deb, 'balance': deb - cre}
		elif deb:
			return {'cre': 0, 'deb': deb, 'balance': deb}
		elif  cre:
			return {'cre': cre, 'deb': 0, 'balance': 0 - cre}
		else: return {'cre': 0, 'deb': 0, 'balance': 0}

class Operation(models.Model):

	TRANS_TYPES = {
		('DEB', "Приход"),
		('CRE', "Расход"),
	}

	kassa = models.ForeignKey(Kassa, related_name='operations',
								on_delete=models.CASCADE, null=True)
	create_date = models.DateTimeField(auto_now_add=True, null=True)
	kid = models.ForeignKey(Kid, related_name='operations',
								on_delete=models.CASCADE,
								null=True, blank=True)
	user = models.ForeignKey(ApiUser, on_delete=models.CASCADE, null=True)
	trans_type = models.CharField(max_length=3, choices=TRANS_TYPES, null=True)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	img = models.ImageField(upload_to='media', blank=True)
	comment = models.CharField(max_length=155, null=True, blank=True)
	update_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return "{} {}".format(self.create_date.date(), str(self.kid))


