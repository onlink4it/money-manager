from django.contrib import admin
from .models import Category,SubCategory,InTransaction,OutTransaction
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(InTransaction)
admin.site.register(OutTransaction)