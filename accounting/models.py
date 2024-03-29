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
    is_charity = models.BooleanField(null=True, default=False)
    is_active = models.BooleanField(null=True, default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "details/%i" % self.id

    def get_cre_sum(self):
        return self.operations.filter(trans_type="CRE").aggregate(Sum('amount'))['amount__sum']

    def get_deb_sum(self):
        return self.operations.filter(trans_type="DEB").aggregate(Sum('amount'))['amount__sum']

    def get_saldo(self):
        cre = self.operations.filter(trans_type="CRE").aggregate(Sum('amount'))['amount__sum']
        deb = self.operations.filter(trans_type="DEB").aggregate(Sum('amount'))['amount__sum']
        return self._get_saldo(deb, cre)

    def get_saldo_from(self, date_from):
        cre = self.operations.filter(trans_type="CRE", create_date__gte=date_from).aggregate(Sum('amount'))['amount__sum']
        deb = self.operations.filter(trans_type="DEB", create_date__gte=date_from).aggregate(Sum('amount'))['amount__sum']
        return self._get_saldo(deb, cre)

    @staticmethod
    def _get_saldo(deb, cre):
        if deb and cre:
            return deb - cre
        elif deb:
            return deb
        else:
            return 0

    def kids_paid(self):
        kids_paid = [kid[0] for kid in self.operations.filter(trans_type="DEB").values_list('kid')]
        return kids_paid

    def kid_balance(self, kid, at=None):
        if at:
            query = {'kassa__is_charity': False, 'kid': kid, 'create_date__gt': at}
        else:
            query = {'kassa__is_charity': False, 'kid': kid}
        cre = self.operations.filter(**query, trans_type="CRE").aggregate(Sum('amount'))['amount__sum']
        deb = self.operations.filter(**query, trans_type="DEB").aggregate(Sum('amount'))['amount__sum']
        if deb and cre:
            return {'cre': cre, 'deb': deb, 'balance': deb - cre}
        elif deb:
            return {'cre': 0, 'deb': deb, 'balance': deb}
        elif cre:
            return {'cre': cre, 'deb': 0, 'balance': 0 - cre}
        else:
            return {'cre': 0, 'deb': 0, 'balance': 0}

    def transfer_to_account(self, amount: float, kid: Kid):
        kid.kid_balance.charge_balance(amount)
        Operation.objects.create(
            amount=amount,
            kassa=self,
            kid=kid,
            trans_type='DEB',
        )

    def transfer_from_account(self, amount: float, kid: Kid):
        kid.kid_balance.withdraw_balance(amount)
        Operation.objects.create(
            amount=amount,
            kassa=self,
            kid=kid,
            trans_type='CRE',
        )


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
