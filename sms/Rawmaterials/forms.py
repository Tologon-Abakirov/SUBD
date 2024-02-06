from django import forms
from .models import RawMaterials

class RawMaterialsForm(forms.ModelForm):

    class Meta:
        model = RawMaterials
        fields = ('Name', 'Unit_of_measurement_id', 'Quantity', 'Amount')