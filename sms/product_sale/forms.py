from django import forms
from .models import ProductSale
from employees.models import Employees
from Currency.models import Currency

class ProductSaleForm(forms.ModelForm):
    class Meta:

        model = ProductSale
        fields = ('Product_id', 'Quantity', 'Amount', 'Currency', 'Date', 'Employee_id')

        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductSaleForm, self).__init__(*args, **kwargs)
        # Добавим выпадающий список для поля 'Employee_id'
        self.fields['Employee_id'] = forms.ModelChoiceField(queryset=Employees.objects.all(), to_field_name='id')

    def __init__(self, *args, **kwargs):
        super(ProductSaleForm, self).__init__(*args, **kwargs)
        # Добавим выпадающий список для поля 'Employee_id'
        self.fields['Currency'] = forms.ModelChoiceField(queryset= Currency.objects.all(), to_field_name='id')



class ProductSaleFormFilter(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
