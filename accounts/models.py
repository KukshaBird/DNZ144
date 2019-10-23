from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class ApiUser(AbstractUser):

	class Meta(AbstractUser.Meta):
		db_table='accounts_user'

	def __str__(self):
		return "@{}".format(self.username)

	def get_group_list(self):
		group_list = []
		for kid in self.kids.all():
			group_list.append(kid.groups.first())
		return group_list

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,
								on_delete=models.CASCADE,
								related_name='profile',
								)
	phone = models.CharField(max_length=10, blank=True, null=True)



	