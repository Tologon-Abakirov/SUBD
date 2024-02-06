from django import forms
from .models import Finishs

class FinishsForm(forms.ModelForm):

    class Meta:
        model = Finishs
        fields = ('Name', 'Unit_of_measurement_id', 'Quantity', 'Amount')