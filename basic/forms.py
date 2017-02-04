from django import forms
from django.contrib.auth.models import User

from .models import Category,SubCategory,InTransaction,OutTransaction


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name',]


class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = ['parent', 'name']


class InTransactionForm(forms.ModelForm):

    class Meta:
        model = InTransaction
        fields = ['sub_cat', 'amount', 'comment', 'date']


class OutTransactionForm(forms.ModelForm):

    class Meta:
        model = OutTransaction
        fields = ['sub_cat', 'amount', 'comment', 'date']




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']