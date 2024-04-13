from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredients
from .forms import IngredientsForm, ProductForm
from finishedproduct.models import Finishs
from django.contrib import messages
from django.db import connection
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



# def ingredients_create(request):
#     if request.method == 'POST':
#         form = IngredientsForm(request.POST)
#         if form.is_valid():
#             product_id = form.cleaned_data['Product_id']
#             raw_material_id = form.cleaned_data['RawMaterial_id']
#
#             # Проверка наличия ингредиента с таким продуктом и сырьем
#             existing_ingredient = Ingredients.objects.filter(Product_id=product_id, RawMaterial_id=raw_material_id).exists()
#
#             if not existing_ingredient:
#                 sale = form.save()
#                 messages.success(request, 'Ингредиент успешно создан.')
#                 return redirect('ingredients_list')
#             else:
#                 messages.error(request, 'Ингредиент с таким продуктом и сырьем уже существует.')
#         else:
#             messages.error(request, 'Форма заполнена некорректно. Пожалуйста, проверьте введенные данные.')
#     else:
#         form = IngredientsForm(initial={'Product_id': request.session.get('product_id')})
#
#     return render(request, 'ingredients_form.html', {'form': form})
# def ingredients_edit(request, pk):
#     ingredient = get_object_or_404(Ingredients, pk=pk)
#     if request.method == 'POST':
#         form = IngredientsForm(request.POST, instance=ingredient)
#         if form.is_valid():
#             product = form.cleaned_data['Product_id']
#             raw_material_id = form.cleaned_data['RawMaterial_id']
#             # ingredient = form.save()
#             # messages.success(request, 'Ингредиент успешно изменен.')
#             # return redirect('ingredients_list')  # Перенаправление на список ингредиентов
#             print(product != ingredient.Product_id or raw_material_id != ingredient.RawMaterial_id)
#             if product == ingredient.Product_id or raw_material_id == ingredient.RawMaterial_id:
#                 print("ing",ingredient.Product_id," ",product)
#                 print("ing",ingredient.RawMaterial_id," ",raw_material_id)
#
#                 existing_ingredient = Ingredients.objects.filter(Product_id=product, RawMaterial_id=raw_material_id).exists()
#                 if not existing_ingredient:
#                     print("changed")
#                     ingredient = form.save()
#                     messages.success(request, 'Ингредиент успешно изменен.')
#                     return redirect('ingredients_list')
#                 else:
#                     messages.error(request, 'Ингредиент с таким продуктом и сырьем уже существует.')
#             else:
#                 print("not changed")
#                 ingredient = form.save()
#                 messages.success(request, 'Ингредиент успешно изменен.')
#                 return redirect('ingredients_list')
#     else:
#         form = IngredientsForm(instance=ingredient)
#
#     return render(request, 'ingredients_edit.html', {'form': form, 'ingredients': ingredient})
#
# def ingredients_delete(request, pk):
#     ingredient = get_object_or_404(Ingredients, pk=pk)
#     ingredient.delete()
#     return redirect('ingredients_list')





def ingredients_create(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['Product_id'].id
            raw_material_id = form.cleaned_data['RawMaterial_id'].id
            quantity = form.cleaned_data['Quantity']
            with connection.cursor() as cursor:
                try:
                    cursor.execute("DECLARE @ErrorCode INT; EXEC CreateIngredient @ProductID=%s, @RawMaterialID=%s, @Quantity=%s, @ErrorCode=@ErrorCode OUTPUT; SELECT @ErrorCode;", [product_id, raw_material_id, quantity])
                    error_code = cursor.fetchone()[0]
                    if error_code == 0:
                        messages.success(request, 'Ингредиент успешно создан.')
                        return redirect('ingredients_list')
                    else:
                        messages.error(request, 'Ингредиент с таким продуктом и сырьем уже существует.')
                except Exception as e:
                    messages.error(request, f'Ошибка выполнения запроса к базе данных: {e}')
                    return redirect('ingredients_list')
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
            product_id = form.cleaned_data['Product_id'].id
            raw_material_id = form.cleaned_data['RawMaterial_id'].id
            quantity = form.cleaned_data['Quantity']
            with connection.cursor() as cursor:
                try:
                    cursor.execute("DECLARE @ErrorCode INT; EXEC EditIngredient @ID=%s, @ProductID=%s, @RawMaterialID=%s, @Quantity=%s, @ErrorCode=@ErrorCode OUTPUT; SELECT @ErrorCode;", [pk, product_id, raw_material_id, quantity])
                    error_code = cursor.fetchone()[0]
                    if error_code == 0:
                        messages.success(request, 'Ингредиент успешно изменен.')
                        return redirect('ingredients_list')
                    else:
                        messages.error(request, 'Ингредиент с таким продуктом и сырьем уже существует.')
                except Exception as e:
                    messages.error(request, f'Ошибка редактирования ингредиента: {e}')
                    return redirect('ingredients_list')
    else:
        form = IngredientsForm(instance=ingredient)

    return render(request, 'ingredients_edit.html', {'form': form, 'ingredients': ingredient})

def ingredients_delete(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    with connection.cursor() as cursor:
        try:
            cursor.execute("DECLARE @ErrorCode INT; EXEC DeleteIngredient @ID=%s, @ErrorCode=@ErrorCode OUTPUT; SELECT @ErrorCode;", [pk])
            error_code = cursor.fetchone()[0]
            if error_code == 0:
                messages.success(request, 'Ингредиент успешно удален.')
            else:
                messages.error(request, 'Ошибка при удалении ингредиента.')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении ингредиента: {e}')
    return redirect('ingredients_list')


