from django.db import models
from django.utils.text import slugify

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
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
	slug = models.SlugField(allow_unicode=True, unique=True)
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



	