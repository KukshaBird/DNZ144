from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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
