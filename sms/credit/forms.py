from django import forms
from .models import Credit, PreCreditPayment


class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ('loan_amount', 'term_months', 'annual_interest_rate', 'penalty', 'date_received')

class PreCreditPaymentForm(forms.ModelForm):
    class Meta:
        model = PreCreditPayment
        fields = ('payment_date', 'principal_amount', 'interest', 'total_amount', 'days_overdue', 'penalty', 'total', 'balance')
