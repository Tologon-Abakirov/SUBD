from django import forms
from .models import Ingredients
from finishedproduct.models import Finishs
class IngredientsForm(forms.ModelForm):


    class Meta:
        model = Ingredients
        fields = ('Product_id', 'RawMaterial_id', 'Quantity',)




class ProductForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ('Product_id',)