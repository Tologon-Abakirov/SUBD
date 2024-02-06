from django import forms
from .models import RawMaterialPurchase
from Rawmaterials.models import RawMaterials
from employees.models import Employees

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = RawMaterialPurchase
        fields = ('RawMaterial_id', 'Quantity', 'Amount', 'Date', 'Employee_id')

        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            super(EmployeeForm, self).__init__(*args, **kwargs)
            # Добавим выпадающий список для поля 'position'
            self.fields['RawmMterial_id'] = forms.ModelChoiceField(queryset=RawMaterials.objects.all(), to_field_name='id')
            self.fields['Employee_id'] = forms.ModelChoiceField(queryset= Employees.objects.all(), to_field_name='id')

class ProductSaleFormFilter(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))