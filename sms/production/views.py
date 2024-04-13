from django.shortcuts import render, get_object_or_404, redirect
from .models import Production
from .forms import ProductionForm, ProductionFormFilter
from django.db.models import Sum
from django.db import connection
from django.contrib import messages
from Ingredients.models import Ingredients
from Rawmaterials.models import RawMaterials
from finishedproduct.models import Finishs


def list(request):
    if request.method == 'POST':
        form = ProductionFormFilter(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            sales = Production.objects.filter(Date__range=[start_date, end_date])
            total_amount = sales.aggregate(total_amount=Sum('Quantity'))['total_amount'] or 0
    else:
        form = ProductionFormFilter()
        sales = Production.objects.all()
        context = {'employees': sales, 'form': form}
        return render(request, 'production_list.html', context)
        total_amount = sales.aggregate(total_amount=Sum('Quantity'))['total_amount'] or 0
        
    context = {'employees': sales, 'form': form, 'total_amount': total_amount}
    return render(request, 'production_list.html', context)
    

# def list(request):
#     employees = Production.objects.all()
#     return render(request, 'production_list.html', {'employees': employees})

def detail(request, pk):
    employee = get_object_or_404(Production, pk=pk)
    return render(request, 'production_detail.html', {'employee': employee})

def check_raw_enough(product_id,quantity):
    try:
        with connection.cursor() as cursor:
            result_param = -1  # Инициализация переменной для хранения значения результата
            cursor.execute("DECLARE @result INT; EXEC CheckRawMaterialAvailability @product_id=%s, @quantity=%s, @result=@result OUTPUT; SELECT @result;",
                           [product_id, quantity])
            result = cursor.fetchone()
            if result:
                result_param = result[0]
            return result_param
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return -1
    return -1 

# def check_is_raw_enough(ingredients,quantity):
#     for ingredient in ingredients:
#         print("ingredint",ingredient.Product_id)
#         total_quantity_needed = ingredient.Quantity * quantity
#         raw_material_quantity=RawMaterials.objects.get(id=ingredient.RawMaterial_id.id).Quantity
#         if total_quantity_needed>raw_material_quantity:
#             return 0
#     return 1
        # raw_material_amount=RawMaterials.objects.get(id=ingredient.RawMaterial_id).Amount
        # raw_material_quantity=RawMaterials.objects.get(id=ingredient.RawMaterial_id).Quantity
        # raw_material_price=raw_material_amount/raw_material_quantity


# def update_raw_and_products(ingredients,quantity):
#     total_amount=0
#     for ingredient in ingredients:
#         raw_material=RawMaterials.objects.get(id=ingredient.RawMaterial_id.id)
#         raw_material_price=raw_material.Amount/raw_material.Quantity
#         total_raw_material_amount=raw_material_price*quantity*ingredient.Quantity
#         total_amount+=total_raw_material_amount
#         raw_material.Quantity-=ingredient.Quantity*quantity
#         raw_material.Amount-=total_raw_material_amount
#         raw_material.save()
#         print("total_raw",total_raw_material_amount)
#     print("total_amount",total_amount)
#     finished_product=Finishs.objects.get(id=ingredient.Product_id.id)
#     finished_product.Amount+=total_amount
#     finished_product.Quantity+=quantity
#     finished_product.save()

# def create(request):
#     if request.method == 'POST':
#         form = ProductionForm(request.POST)
#         if form.is_valid():
#             product_id = form.cleaned_data['Product_id'].id
#             quantity = form.cleaned_data['Quantity']
#             ingredients = Ingredients.objects.filter(Product_id=product_id)
#             is_raw_enough = check_is_raw_enough(ingredients,quantity)
#             if is_raw_enough:
#                 update_raw_and_products(ingredients,quantity)
#                 employee = form.save(commit=False)
#                 employee.save()
#                 return redirect('production_list')
#             else:
#                 messages.error(request, 'Не достаточно сьрья для производства.')
#         else:
#             messages.error(request, 'Форма содержит ошибки.')
#     else:
#         form = ProductionForm()
#     return render(request, 'production_form.html', {'form': form})

# def edit(request, pk):
#     employee = get_object_or_404(Production, pk=pk)
#     if request.method == 'POST':
#         form = ProductionForm(request.POST, instance=employee)
#         if form.is_valid():
#             employee = form.save(commit=False)
#             employee.save()
#             return redirect('production_list')
#     else:
#         form = ProductionForm(instance=employee)
#     return render(request, 'production_edit.html', {'form': form, 'employee': employee})

# def delete(request, pk):
#     employee = get_object_or_404(Production, pk=pk)
#     employee.delete()
#     return redirect('production_list')


def delete(request, pk):
    with connection.cursor() as cursor:
        try:
            cursor.execute("EXEC DeleteProduction @ProductionID=%s", [pk])
            return redirect('production_list')
        except Exception as e:
            messages.error(request, f'Ошибка удаления записи: {e}')
            return redirect('production_list')




def create(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['Product_id'].id
            quantity = form.cleaned_data['Quantity']
            employee_id = form.cleaned_data['Employee_id'].id
            date = form.cleaned_data['Date']
            is_raw_enough = check_raw_enough(product_id, quantity)
            if is_raw_enough:
                with connection.cursor() as cursor:
                    try:

                        cursor.execute("EXEC UpdateRawMaterialsAndProducts @ProductID=%s, @Quantity=%s", [product_id, quantity])
                        cursor.execute("EXEC CreateProduction @ProductID=%s, @Quantity=%s, @Date=%s, @EmployeeID=%s", [product_id, quantity, date, employee_id])
                        #cursor.execute("EXEC dbo.UpdateCommonAndGeneralProcedure")
                        # employee = form.save(commit=False)
                        # employee.save()
                        
                        return redirect('production_list')
                    except Exception as e:
                        messages.error(request, f'')
            else:
                messages.error(request, 'Не достаточно сырья для производства.')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        form = ProductionForm()
    return render(request, 'production_form.html', {'form': form})



def edit(request, pk):
    employee = get_object_or_404(Production, pk=pk)
    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=employee)
        if form.is_valid():
            product_id = form.cleaned_data['Product_id'].id
            quantity = form.cleaned_data['Quantity']
            with connection.cursor() as cursor:
                try:
                    cursor.execute("EXEC EditProduction @ProductionID=%s, @ProductID=%s, @Quantity=%s", [pk, product_id, quantity])

                    employee = form.save(commit=False)
                    employee.save()
                    return redirect('production_list')
                except Exception as e:
                    messages.error(request, f'Ошибка редактирования записи: {e}')
    else:
        form = ProductionForm(instance=employee)
    return render(request, 'production_edit.html', {'form': form, 'employee': employee})
