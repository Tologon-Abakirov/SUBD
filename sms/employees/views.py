from django.contrib.auth.decorators import login_required
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

@login_required
def profile_views(request):
    return render(request, 'employees/profile.html')

#
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        # Обработка входа пользователя
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправление на страницу профиля
            return redirect('profile')  # замените 'profile' на имя вашего URL-маршрута для страницы профиля
        else:
            # Обработка ошибки входа
            return render(request, 'login.html', {'error_message': 'Invalid login'})  # замените 'login.html' на имя вашего шаблона входа
    else:
        return render(request, 'login.html')  # замените 'login.html' на имя вашего шаблона входа
