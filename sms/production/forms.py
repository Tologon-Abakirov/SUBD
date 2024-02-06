from django import forms
from .models import Production
from employees.models import Employees

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ('Product_id', 'Quantity', 'Date', 'Employee_id')

        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
        }

        def init(self, *args, **kwargs):
            super(ProductionForm, self).init(*args, **kwargs)
            # Добавим выпадающий список для поля 'position'
            self.fields['Employee_id'] = forms.ModelChoiceField(queryset= Employees.objects.all(), to_field_name='id')

class ProductionFormFilter(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))