from django import forms
from django.contrib.auth.models import User

from .models import customer,item,invoice,invoice_items,invoice_setting


class customerForm(forms.ModelForm):

    class Meta:
        model = customer
        fields = ['name','mobile','address','mail']


class itemForm(forms.ModelForm):

    class Meta:
        model = item
        fields = ['name', 'price']


class invoiceForm(forms.ModelForm):

    class Meta:
        model = invoice
        fields = ['date', 'customer', 'is_paid', 'comment']


class invoice_itemsForm(forms.ModelForm):

    class Meta:
        model = invoice_items
        fields = ['invoice_id', 'item', 'quantity', 'unit_price']

class invoice_settingForm(forms.ModelForm):

    class Meta:
        model = invoice_setting
        fields = ['logo']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']