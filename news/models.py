from django.db import models
from django.utils import timezone
from group.models import Group
from django.conf import settings

class News(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=155)
	message = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	access_to = models.ManyToManyField(Group, related_name='news')


	def __str__(self):
		return self.title

class Comment(models.Model):
    news = models.ForeignKey(News, related_name='news_comments', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_news_comments',on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)