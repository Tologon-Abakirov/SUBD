from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductSale
from .forms import ProductSaleForm, ProductSaleFormFilter
from datetime import date
from django.db.models import Sum
from budget.models import Budget
from finishedproduct.models import Finishs
from Ingredients.models import Ingredients
from Rawmaterials.models import RawMaterials
from django.contrib import messages
from django.db import connection

# def sale_list(request):
#     sales = ProductSale.objects.all()
#     return render(request, 'sale_list.html', {'sales': sales})

def sale_list(request):
    if request.method == 'POST':
        form = ProductSaleFormFilter(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            sales = ProductSale.objects.filter(Date__range=[start_date, end_date])
            total_amount = sales.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0
    else:
        form = ProductSaleFormFilter()
        sales = ProductSale.objects.all()
        total_amount = sales.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0

    context = {'sales': sales, 'form': form, 'total_amount': total_amount}
    return render(request, 'sale_list.html', context)

def sale_detail(request, pk):
    sale = get_object_or_404(ProductSale, pk=pk)
    return render(request, 'sale_detail.html', {'sale': sale})

# def update_finishedproducts_quantity(finished_product_id, clean_amount, quantity):
#     finished_product = Finishs.objects.get(id=finished_product_id)
#     finished_product.Quantity -= quantity
#     finished_product.Amount -= clean_amount
#     finished_product.save()
#
# def sale_create(request):
#     if request.method == 'POST':
#         form = ProductSaleForm(request.POST)
#         if form.is_valid():
#             #Получение данных с формы
#             # percent = form.cleaned_data['Percent']
#             quantity = form.cleaned_data['Quantity']
#             finished_product_id = form.cleaned_data['Product_id'].id
#             finished_product = Finishs.objects.get(id=finished_product_id)
#
#             if quantity<finished_product.Quantity:
#                 sale = form.save(commit=False)
#
#                 budget = Budget.objects.first()
#                 percent=budget.Percent
#
#                 #Подсет суммы и обновление бюджета
#                 amount=0
#                 finished_product_price=finished_product.Amount/finished_product.Quantity
#                 amount+=finished_product_price*quantity
#                 clean_amount=amount
#                 amount=amount+(amount*(percent/100))
#                 print("amount ",amount)
#                 print(budget.Budget_Amount)
#                 budget.Budget_Amount += amount
#                 budget.save()
#                 sale.Amount=amount
#                 sale.save()
#
#                 #Обновление готовой продукций
#                 update_finishedproducts_quantity(finished_product_id, clean_amount, quantity)
#                 return redirect('sale_list')
#             else:
#                 messages.error(request, 'Недостаточно количества для проведения операции.')
#         else:
#             # если форма невалидна
#             messages.error(request, 'Форма содержит ошибки.')
#     else:
#         form = ProductSaleForm()
#
#     return render(request, 'sale_form.html', {'form': form})

# def sale_edit(request, pk):
#     sale = get_object_or_404(ProductSale, pk=pk)
#     if request.method == 'POST':
#         form = ProductSaleForm(request.POST, instance=sale)
#         if form.is_valid():
#             sale = form.save()
#             return redirect('sale_list')
#     else:
#         form = ProductSaleForm(instance=sale)
#     return render(request, 'sale_edit.html', {'form': form, 'sale': sale})
#
# def sale_delete(request, pk):
#     sale = get_object_or_404(ProductSale, pk=pk)
#     sale.delete()
#     return redirect('sale_list')



def sale_create(request):
    if request.method == 'POST':
        form = ProductSaleForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['Quantity']
            finished_product_id = form.cleaned_data['Product_id'].id
            employee_id = form.cleaned_data['Employee_id'].id
            date = form.cleaned_data['Date']
            with connection.cursor() as cursor:
                try:
                    cursor.execute("EXEC CreateSaleAndUpdateFinishedProducts @ProductID=%s, @Quantity=%s, @Date=%s, @EmployeeID=%s", [finished_product_id, quantity, date, employee_id])
                    #cursor.execute("EXEC dbo.UpdateCommonAndGeneralProcedure")
                    return redirect('sale_list')
                except Exception as e:
                    messages.error(request, f'Ошибка при создании продажи: {e}')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        form = ProductSaleForm()

    return render(request, 'sale_form.html', {'form': form})




def sale_edit(request, pk):
    sale = get_object_or_404(ProductSale, pk=pk)
    if request.method == 'POST':
        form = ProductSaleForm(request.POST, instance=sale)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC EditProductSale @ID=%s, @ProductID=%s, @Quantity=%s, @Amount=%s, @Date=%s, @EmployeeID=%s", [pk, form.cleaned_data['Product_id'].id, form.cleaned_data['Quantity'], form.cleaned_data['Amount'], form.cleaned_data['Date'], form.cleaned_data['Employee_id'].id])
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'sale_edit.html', {'form': form, 'sale': sale})

            return redirect('sale_list')
    else:
        form = ProductSaleForm(instance=sale)
    return render(request, 'sale_edit.html', {'form': form, 'sale': sale})


def sale_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC DeleteProductSale @ID=%s", [pk])
    except Exception as e:
        messages.error(request, str(e))

    return redirect('sale_list')


