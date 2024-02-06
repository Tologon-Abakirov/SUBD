from django import forms
from .models import Employees, Positions

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employees
        fields = ('Full_Name', 'Position', 'Salary', 'Address', 'Phone')

        def __init__(self, *args, **kwargs):
            super(EmployeeForm, self).__init__(*args, **kwargs)
            # Добавим выпадающий список для поля 'position'
            self.fields['Position'] = forms.ModelChoiceField(queryset=Positions.objects.all(), to_field_name='id')
