from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
class customer(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
	name = models.CharField(max_length = 64)
	mobile = models.CharField(max_length = 11, blank = True , null= True)
	address  = models.CharField(max_length = 256, blank = True , null= True)
	mail = models.CharField(max_length = 64, blank = True , null= True)
	def __str__(self):
		return self.name + " - " + self.mobile + " - " + self.address + " - " + self.mail
	
class item(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
	name = models.CharField(max_length = 64)
	price = models.FloatField( blank = True , null= True)
	def __str__(self):
		return self.name + " - " + str(self.price )


class invoice(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
	date = models.DateField()
	customer = models.ForeignKey(customer, on_delete  = models.CASCADE)
	is_paid = models.BooleanField(default = False)
	comment = models.CharField(max_length = 256 , default = "" , null = True , blank = True)

	def __str__(self):
		return str(self.id) + " - " + str(self.date) + " - " + str(self.customer.name)

	def get_items(self):
		invoice_items.objects.filter(invoice_id = self.id)
	
class invoice_items(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
	invoice_id = models.ForeignKey(invoice, on_delete = models.CASCADE)
	item = models.ForeignKey(item, on_delete = models.CASCADE)
	quantity = models.IntegerField()
	unit_price = models.FloatField()
	total_price = models.FloatField(default = 0)
	
	def __str__(self):
		return str(self.invoice_id.id) + " - " + str(self.item.name) + " - " + str(self.quantity) + " - " + str(self.unit_price)

	def total(self):
		return self.quantity * self.unit_price

class invoice_setting(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE,default =1,unique=True)
	logo = models.FileField()
