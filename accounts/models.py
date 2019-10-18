from django.contrib import auth
from django.db import models


# class Parent(models.Model):
#     name = models.CharField(max_length=50, null=True)

# class Group(models.Model):
#     name = models.CharField(max_length=128, null=True)
#     parents = models.ManyToManyField(
#         Parent,
#         through='Kid',
#         through_fields=('group', 'parent'),
#     )

# class Kid(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
#     parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)





class Group(models.Model):
	name = models.CharField(max_length=30, null=True)
	def __str__(self):
		return self.name

class Family(models.Model):
	name = models.CharField(max_length=30, null=True, default='Family')
	def __str__(self):
		return str(self.id)

class Parent(models.Model):
	first_name = models.CharField(max_length=30, null=True)
	last_name = models.CharField(max_length=30, null=True)
	family = models.ForeignKey(Family, related_name='adults', on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.first_name +self.last_name

class Kid(models.Model):
	first_name = models.CharField(max_length=30, null=True)
	last_name = models.CharField(max_length=30, null=True)
	group = models.ForeignKey(Group, related_name='kids', on_delete=models.CASCADE, null=True)
	family = models.ForeignKey(Family, related_name='siblings', on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.first_name + self.last_name








class User(auth.models.User, auth.models.PermissionsMixin):

	kid = models.OneToOneField(Kid, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return "@{}".format(self.username)



	