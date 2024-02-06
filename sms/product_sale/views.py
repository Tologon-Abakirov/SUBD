from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductSale
from .forms import ProductSaleForm, ProductSaleFormFilter
from datetime import date
from django.db.models import Sum
from django.db import connection
from django.contrib import messages
# def sale_list(request):
#     sales = ProductSale.objects.all()
#     return render(request, 'sale_list.html', {'sales': sales})


def sale_create(request):
    if request.method == 'POST':
        form = ProductSaleForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['Product_id'].id
            quantity = form.cleaned_data['Quantity']
            #Currency = form.cleaned_data['Currency']
            is_product_enough = check_product_enough(product_id, quantity, )
            print(is_product_enough)
            if is_product_enough:
                sell_result = sell_product(product_id, quantity)
                if sell_result:
                    product_sale = form.save(commit=False)
                    product_sale.save()
                    return redirect('sale_detail', pk=product_sale.pk)
                else:
                    messages.error(request, 'Не удалось осуществить продажу.')
            else:
                messages.error(request, 'Не хватает продукта на складе.')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        form = ProductSaleForm()
    return render(request, 'sale_form.html', {'form': form})


def check_product_enough(product_id, quantity):
    try:
        with connection.cursor() as cursor:
            result_param = -1  # Инициализация переменной для хранения значения результата
            cursor.execute("DECLARE @result INT; EXEC CheckProductAvailability @product_id=%s, @quantity=%s, @result=@result OUTPUT; SELECT @result;",
                           [product_id, quantity])
            result = cursor.fetchone()
            if result:
                result_param = result[0]
            return result_param
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return -1
    return -1

def sell_product(product_id, quantity):
    try:
        with connection.cursor() as cursor:
            result_param = -1  # Инициализация переменной для хранения значения результата
            cursor.execute("DECLARE @result INT; EXEC SellProduct @product_id=%s, @quantity=%s, @result=@result OUTPUT; SELECT @result;",
                           [product_id, quantity])
            result = cursor.fetchone()
            if result:
                result_param = result[0]
            return result_param
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return -1
    return -1










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

# def sale_create(request):
#     if request.method == 'POST':
#         form = ProductSaleForm(request.POST)
#         if form.is_valid():
#             sale = form.save()
#             return redirect('sale_detail', pk=sale.pk)
#     else:
#         form = ProductSaleForm()
#     return render(request, 'sale_form.html', {'form': form})

def sale_edit(request, pk):
    sale = get_object_or_404(ProductSale, pk=pk)
    if request.method == 'POST':
        form = ProductSaleForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save()
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = ProductSaleForm(instance=sale)
    return render(request, 'sale_edit.html', {'form': form, 'sale': sale})

def sale_delete(request, pk):
    sale = get_object_or_404(ProductSale, pk=pk)
    sale.delete()
    return redirect('sale_list')
