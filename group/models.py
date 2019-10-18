from django.db import models
from django.utils.text import slugify

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()


class Group(models.Model):
	name = models.CharField(max_length=30, unique=True)
	slug = models.SlugField(allow_unicode=True, unique=True)
	parrents = models.ManyToManyField(
        User,
        through='Child',
    )

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name

class Child(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	group = models.OneToOneField(Group, related_name="group_member",
									on_delete=models.CASCADE,
									unique=True)
	parrents = models.ForeignKey(User,related_name='users_child',on_delete=models.CASCADE, null=True)
	

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)
