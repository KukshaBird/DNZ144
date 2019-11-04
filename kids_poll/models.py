from django.db import models
from django.db.models.manager import Manager

from group.models import Kid, Group

class Poll(models.Model):
    question = models.CharField(max_length=255, unique=True)
    is_published = models.BooleanField(default=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"

    def __str__(self):
        return self.question

    def get_vote_count(self):
        return Vote.objects.filter(poll=self).count()
    vote_count = property(fget=get_vote_count)

class Item(models.Model):
    value = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.value

    def get_vote_count(self):
        return Vote.objects.filter(item=self).count()
    vote_count = property(fget=get_vote_count)


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name='voted item', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='ip address', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return self.kid.__str__()