from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
class Category(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
	name = models.CharField(max_length = 64)
	def __str__(self):
		return self.name
class SubCategory(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
	parent = models.ForeignKey(Category, on_delete = models.CASCADE)
	name = models.CharField(max_length = 64)
	def __str__(self):
		return str(self.parent) + " - " +self.name
class InTransaction(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default=1)
	sub_cat = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
	amount = models.FloatField(default= 0 )
	comment = models.CharField(max_length = 256)
	date = models.DateField()
	def __str__(self):
		return "Income : Category[" + str(self.sub_cat) + "] - Amount[" + str(self.amount) + "] - Comment[" + self.comment + "] - Date[" + str(self.date)+"]"
class OutTransaction(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default=1)
	sub_cat = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
	amount = models.FloatField(default= 0 )
	comment = models.CharField(max_length = 256)
	date = models.DateField()
	def __str__(self):
		return "Outcome : Category[" + str(self.sub_cat) + "] - Amount[" +str(self.amount) + "] - Comment[" + self.comment + "] - Date[" + str(self.date)+"]"