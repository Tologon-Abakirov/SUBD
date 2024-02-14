from django.shortcuts import render, get_object_or_404, redirect
from .models import RawMaterialPurchase
from .forms import EmployeeForm, ProductSaleFormFilter
from django.db.models import Sum
from datetime import date
from django.db import connection
from django.contrib import messages
from django.http import HttpResponseServerError
from budget.models import Budget
from Rawmaterials.models import RawMaterials



def list(request):
    if request.method == 'POST':
        form = ProductSaleFormFilter(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            employees = RawMaterialPurchase.objects.filter(Date__range=[start_date, end_date])
            total_amount = employees.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0
    else:
        form = ProductSaleFormFilter()
        employees = RawMaterialPurchase.objects.all()
        total_amount = employees.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0

    context = {'employees': employees, 'form': form, 'total_amount': total_amount}

    return render(request, 'rawSale_list.html', context)
def detail(request, pk):
    employee = get_object_or_404(RawMaterialPurchase, pk=pk)
    return render(request, 'rawSale_detail.html', {'employee': employee})

# def check_budget_enough(amount):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("DECLARE @result INT; EXEC @result = IsBudgetEnough @amount=%s; SELECT @result;", [amount])
#             result = cursor.fetchone()
#             if result:
#                 return result[0]
#     except Exception as e:
#         print(f"Error executing SQL: {e}")
#         return -1
#     return -1

def update_budget(amount):
    budget = Budget.objects.first()
    budget.Budget_Amount -= amount
    budget.save()

def update_raw_materials_quantity(raw_material_id, amount, quantity):
    raw_material = RawMaterials.objects.get(id=raw_material_id)
    raw_material.Quantity += quantity
    raw_material.Amount += amount
    raw_material.save()

def create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['Amount']
            quantity = form.cleaned_data['Quantity']
            raw_material_id = form.cleaned_data['RawMaterial_id'].id
            budget = Budget.objects.first()
            is_budget_enough = budget.Budget_Amount<amount

            if not is_budget_enough:
                employee = form.save(commit=False)
                employee.save()
                update_budget(amount)
                update_raw_materials_quantity(raw_material_id, amount, quantity)
                return redirect('rawSale_list')
            else:
                messages.error(request, 'Бюджет недостаточен для проведения операции.')
        else:
            # если форма невалидна
            messages.error(request, 'Форма содержит ошибки.')
    else:
        form = EmployeeForm()

    return render(request, 'rawSale_form.html', {'form': form})


def edit(request, pk):
    employee = get_object_or_404(RawMaterialPurchase, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect('rawSale_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'rawSale_edit.html', {'form': form, 'employee': employee})

def delete(request, pk):
    employee = get_object_or_404(RawMaterialPurchase, pk=pk)
    employee.delete()
    return redirect('rawSale_list')