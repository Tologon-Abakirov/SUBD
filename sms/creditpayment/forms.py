from django import forms
from .models import CreditPayment

class CreditPaymentForm(forms.ModelForm):
    class Meta:
        model = CreditPayment
        fields = ('payment_date', 'principal_amount', 'interest', 'total_amount', 'days_overdue', 'penalty', 'total', 'balance')
