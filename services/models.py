from django.db import models
from django.utils import timezone
from group.models import Group
from kids_poll.models import Poll
from django.conf import settings

class IssuesModel(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=155)
	description = models.TextField(blank=True, null=True)
	is_closed = models.BooleanField(default=False)
	created_date = models.DateTimeField(default=timezone.now)
	closed_date = models.DateTimeField(blank=True, null=True)
	access_to = models.ManyToManyField(Group, related_name='issues')
	img = models.ImageField(upload_to='media', blank=True, null=True)


	def __str__(self):
		return self.title

	def close_issue(self):
		self.closed_date = timezone.now()
		self.is_closed = True
		self.save()

class Comment(models.Model):
    issue = models.ForeignKey(IssuesModel, related_name='issue_comments', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_issue_comments',on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

class IssuePoll(models.Model):
    issue = models.ForeignKey(IssuesModel, related_name='polls', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issue_polls',on_delete=models.CASCADE, null=True, blank=True)
    poll = models.ForeignKey(Poll, related_name='to_issue',on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

