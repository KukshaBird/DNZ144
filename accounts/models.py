from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.db.models import signals


def user_created(sender, instance, created, **kwargs):
    if created:
        AccountBalance.objects.create(user=instance)


class ApiUser(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True,
                             unique=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = 'accounts_user'

    def __str__(self):
        return "@{}".format(self.username)

    def get_absolute_url(self):
        return reverse('accounts:account_detail', args=[str(self.id)])

    def get_group_list(self):
        group_list = []
        for kid in self.kids.all():
            group_list.append(kid.groups.first())
        return group_list

    def has_group(self):
        if len(self.get_group_list()) > 0:
            return True
        return False

    def get_balanse(self):
        from accounting.models import Kassa
        balance = 0
        if len(self.get_group_list()) > 0:
            for kassa in Kassa.objects.filter(group=self.get_group_list()[0]):
                # TODO: KID FIRST???
                if kassa.kid_balance(self.kids.first()):
                    balance += kassa.kid_balance(self.kids.first())['balance']
            return balance


class AccountBalance(models.Model):
    user = models.OneToOneField(ApiUser, on_delete=models.CASCADE, related_name='account_balance', blank=True,
                                null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def charge_balance(self, amount: float):
        self.amount += amount

    def withdraw_balance(self, amount: float):
        self.amount -= amount

    def __str__(self):
        return f'{self.user} - {self.amount}'


signals.post_save.connect(receiver=user_created, sender=ApiUser)
