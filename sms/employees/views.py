from django.shortcuts import render, get_object_or_404, redirect
from .models import Employees
from .forms import EmployeeForm
from budget.models import Budget
def list(request):
    employees = Employees.objects.all()
    return render(request, 'list.html', {'employees': employees})

def detail(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    return render(request, 'detail.html', {'employee': employee})

def create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect('list')
    else:
        form = EmployeeForm()
    return render(request, 'form.html', {'form': form})

def edit(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect('list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit.html', {'form': form, 'employee': employee})

def delete(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    employee.delete()
    return redirect('list')
