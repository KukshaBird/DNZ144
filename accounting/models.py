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

	def get_cre_sum(self):
		return self.operations.filter(trans_type="CRE").aggregate(Sum('amount'))['amount__sum']

	def get_deb_sum(self):
		return self.operations.filter(trans_type="DEB").aggregate(Sum('amount'))['amount__sum']

	def get_saldo(self):
		cre = self.operations.filter(trans_type="CRE").aggregate(Sum('amount'))['amount__sum']
		deb = self.operations.filter(trans_type="DEB").aggregate(Sum('amount'))['amount__sum']
		return deb - cre

	def user_paid(self):
		kids_paid = [kid[0] for kid in self.operations.filter(trans_type="DEB").values_list('kid')]
		return kids_paid

class Operation(models.Model):

	TRANS_TYPES = {
		('DEB', "Приход"),
		('CRE', "Расход"),
		('TRA', "Перевод"),
		('BAL', "Баланс"),
	}

	kassa = models.ForeignKey(Kassa, related_name='operations',
								on_delete=models.CASCADE, null=True)
	create_date = models.DateTimeField(auto_now_add=True, null=True)
	kid = models.ForeignKey(Kid, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(ApiUser, on_delete=models.CASCADE, null=True, blank=True)
	trans_type = models.CharField(max_length=3, choices=TRANS_TYPES, null=True)
	amount = models.IntegerField()
	img = models.ImageField(upload_to='media', blank=True)
	comment = models.CharField(max_length=155, null=True, blank=True)

	def __str__(self):
		return str(self.create_date)


