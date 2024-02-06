from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredients
from .forms import IngredientsForm, ProductForm
from finishedproduct.models import Finishs
from django.contrib import messages
def ingredients_list(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['Product_id']
            pr_id = Finishs.objects.get(Name=product)

            request.session['product_id'] = pr_id.id

            ingredients = Ingredients.objects.filter(Product_id=product)
    else:
        product_id = request.session.get('product_id')
        if product_id is not None:
            form = ProductForm(initial={'Product_id': product_id})
            ingredients = Ingredients.objects.filter(Product_id=product_id)
        else:
            form = ProductForm()
            ingredients = Ingredients.objects.all()

    context = {'ingredients': ingredients, 'form': form}
    return render(request, 'ingredients_list.html', context)

def ingredients_detail(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    return render(request, 'ingredients_detail.html', {'ingredient': ingredient})



def ingredients_create(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['Product_id']
            raw_material_id = form.cleaned_data['RawMaterial_id']

            # Проверка наличия ингредиента с таким продуктом и сырьем
            existing_ingredient = Ingredients.objects.filter(Product_id=product_id, RawMaterial_id=raw_material_id).exists()

            if not existing_ingredient:
                sale = form.save()
                messages.success(request, 'Ингредиент успешно создан.')
                return redirect('ingredients_list')
            else:
                messages.error(request, 'Ингредиент с таким продуктом и сырьем уже существует.')
        else:
            messages.error(request, 'Форма заполнена некорректно. Пожалуйста, проверьте введенные данные.')
    else:
        form = IngredientsForm(initial={'Product_id': request.session.get('product_id')})

    return render(request, 'ingredients_form.html', {'form': form})
def ingredients_edit(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    if request.method == 'POST':
        form = IngredientsForm(request.POST, instance=ingredient)
        if form.is_valid():
            ingredient = form.save()
            messages.success(request, 'Ингредиент успешно изменен.')
            return redirect('ingredients_list')  # Перенаправление на список ингредиентов
    else:
        form = IngredientsForm(instance=ingredient)

    return render(request, 'ingredients_edit.html', {'form': form, 'ingredients': ingredient})

def ingredients_delete(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    ingredient.delete()
    return redirect('ingredients_list')
