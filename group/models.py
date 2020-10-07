from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import signals
from django.utils.text import slugify
from django import template

def kid_created(sender, instance, created, **kwargs):
    if created:
        KidBalance.objects.create(kid=instance)


User = get_user_model()
register = template.Library()


class Kid(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    parents = models.ManyToManyField(User, related_name='kids', related_query_name="kid", blank=True)

    def __str__(self):
        return "%s (%s)" % (
            self.last_name,
            ", ".join(parent.username for parent in self.parents.all()),
        )


class Group(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    kids = models.ManyToManyField(Kid, related_name='groups', blank=True)
    number = models.PositiveSmallIntegerField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Staff(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s № %s" % (self.first_name, self.group.name, self.group.number)


class KidBalance(models.Model):
    kid = models.OneToOneField(Kid, on_delete=models.CASCADE, related_name='kid_balance', blank=True,
                               null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def charge_balance(self, amount: float):
        self.amount += amount
        self.save()

    def withdraw_balance(self, amount: float):
        self.amount -= amount
        self.save()

    def __str__(self):
        return f'{self.kid} - {self.amount}'


signals.post_save.connect(receiver=kid_created, sender=Kid, weak=True)
