from django import forms
from django.forms import ModelForm
from .models import Bond

class BondForm(ModelForm):
    class Meta:
        model = Bond
        fields = ('cusip', 'face', 'coupon', 'payments_per_year', 'initial_price', 'auction_date', 'dated_date', 'maturity',)
        # widgets = {
        #     'username': forms.TextInput({'class':'form-control'}),
        #     'email': forms.TextInput({'class':'form-control'}),
        #     'password': forms.PasswordInput({'class':'form-control'}),
        # }