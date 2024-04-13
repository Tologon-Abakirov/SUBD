from django import forms
from .models import ProductSale
from employees.models import Employees

class ProductSaleForm(forms.ModelForm):
    class Meta:
        model = ProductSale
        fields = ('Product_id', 'Quantity', 'Date', 'Employee_id')
        def init(self, *args, **kwargs):
            super(ProductSaleForm, self).init(*args, **kwargs)
            # Добавим выпадающий список для поля 'position'
            self.fields['Employee_id'] = forms.ModelChoiceField(queryset= Employees.objects.all(), to_field_name='id')

class ProductSaleFormFilter(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))