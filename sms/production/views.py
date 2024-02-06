from django.shortcuts import render, get_object_or_404, redirect
from .models import Production
from .forms import ProductionForm, ProductionFormFilter
from django.db.models import Sum
from django.db import connection
from django.contrib import messages

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

def create(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['Product_id'].id
            quantity = form.cleaned_data['Quantity']
            is_raw_enough = check_raw_enough(product_id,quantity)
            print(is_raw_enough)
            if is_raw_enough:
                employee = form.save(commit=False)
                employee.save()
                return redirect('production_detail', pk=employee.pk)
            else:
                messages.error(request, 'Не достаточно сьрья для производства.')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        form = ProductionForm()
    return render(request, 'production_form.html',{'form': form})


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


def edit(request, pk):
    employee = get_object_or_404(Production, pk=pk)
    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect('production_detail', pk=employee.pk)
    else:
        form = ProductionForm(instance=employee)
    return render(request, 'production_edit.html', {'form': form, 'employee': employee})

def delete(request, pk):
    employee = get_object_or_404(Production, pk=pk)
    employee.delete()
    return redirect('production_list')
