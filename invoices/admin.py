from django.contrib import admin
from .models import customer, item, invoice,invoice_items,invoice_setting
# Register your models here.
admin.site.register(customer)
admin.site.register(item)
admin.site.register(invoice)
admin.site.register(invoice_items)
admin.site.register(invoice_setting)