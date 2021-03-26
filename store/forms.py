from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.shortcuts import render

from .models import *
from django import forms


class StoreUserForm(ModelForm):
    confirm_pass = forms.CharField(max_length=100)

    class Meta:
        model = StoreUser
        fields = ('username', 'password', 'confirm_pass')

    def clean(self):
        clean_data = super().clean()
        if clean_data.get('password') != clean_data.get('confirm_pass'):
            raise forms.ValidationError('Passwords are not equal!')


class SnusCreateForm(ModelForm):
    class Meta:
        model = Snus
        fields = ('title', 'description', 'picture', 'quantity', 'price')


class SnusUpdateForm(ModelForm):
    class Meta:
        model = Snus
        fields = ('title', 'description', 'picture', 'quantity', 'price')

class SnusPurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ('quantity',  )

class SnusReturnForm(ModelForm):
    class Meta:
        model = ReturnPurchase
        fields = ()