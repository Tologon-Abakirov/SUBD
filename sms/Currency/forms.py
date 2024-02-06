from django import forms
from sms.Currency.models import Currency

class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency
        fields = ('Name',)
