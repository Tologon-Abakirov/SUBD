from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Salary
from .forms import SalaryForm, SalaryFormFilter
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Sum
import datetime
import requests

# def salary_list(request):
#     salaryes = Salary.objects.all()
#     print("salaries ", salaryes)
#
#     total_amount = salaryes.aggregate(total_amount=Sum('General'))['total_amount'] or 0
#     context = {'salaryes': salaryes, 'total_amount': total_amount}
#     return render(request, 'salary_list.html', {'salaryes': salaryes}, context)

# def salary_list(request):
#     # Получаем все записи зарплат
#     salaryes = Salary.objects.all()
#
#     # Извлекаем уникальные года из полей Year в записях зарплат
#     years = salaryes.values_list('Year', flat=True).distinct()
#
#     # Фильтрация записей по выбранным году и месяцу
#     selected_year = request.GET.get('year')
#     selected_month = request.GET.get('month')
#     if selected_year:
#         salaryes = salaryes.filter(Year=selected_year)
#     if selected_month:
#         salaryes = salaryes.filter(Month=selected_month)
#
#     return render(request, 'salary_list.html', {'salaryes': salaryes, 'years': years})


# def salary_list(request):
#     # Получаем текущий год и месяц
#     current_year = datetime.datetime.now().year
#     current_month = datetime.datetime.now().month
#
#     # Получаем все записи зарплат
#     salaryes = Salary.objects.all()
#
#     # Извлекаем уникальные года из полей Year в записях зарплат
#     years = salaryes.values_list('Year', flat=True).distinct()
#
#     # Фильтрация записей по выбранным году и месяцу, с учетом текущего года и месяца по умолчанию
#     selected_year = request.GET.get('year', current_year)
#     selected_month = request.GET.get('month', current_month)
#     if selected_year:
#         salaryes = salaryes.filter(Year=selected_year)
#     if selected_month:
#         salaryes = salaryes.filter(Month=selected_month)
#
#     # Вычисление общей суммы только для невыданных зарплат
#     total_amount = salaryes.filter(Given=False).aggregate(total_amount=Sum('General'))['total_amount'] or 0
#
#     return render(request, 'salary_list.html', {'salaryes': salaryes, 'years': years, 'current_year': current_year, 'current_month': current_month, 'total_amount': total_amount})

def salary_list(request):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    selected_year = request.GET.get('year', current_year)
    selected_month = request.GET.get('month', current_month)

    total_amount = 0

    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC UpdateCommonAndGeneralProcedure @Year=%s, @Month=%s", [selected_year, selected_month])
            row = cursor.fetchone()
            if row:
                total_amount = row[0]
    except Exception as e:
        messages.error(request, 'Ошибка при выполнении запроса к базе данных: {}'.format(str(e)))

    # Получаем записи зарплат для выбранного года и месяца
    salaryes = Salary.objects.filter(Year=selected_year, Month=selected_month)

    # Check if all salaries for the selected period are given
    all_salaries_given = all(salary.Given for salary in salaryes)

    return render(request, 'salary_list.html', {'salaryes': salaryes, 'total_amount': total_amount, 'all_salaries_given': all_salaries_given})

def salary_detail(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    return render(request, 'salary_detail.html', {'salary': salary})

def salary_create(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save()
            return redirect('salary_list')
    else:
        form = SalaryForm()
    return render(request, 'salary_form.html', {'form': form})

# Без хранимок
# def salary_edit(request, pk):
#     salary = get_object_or_404(Salary, pk=pk)
#     if request.method == 'POST':
#         form = SalaryForm(request.POST, instance=salary)
#         if form.is_valid():
#             salary = form.save()
#             return redirect('salary_list')
#     else:
#         form = SalaryForm(instance=salary)
#     return render(request, 'salary_edit.html', {'form': form, 'salary': salary})
#
def salary_delete(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    salary.delete()
    return redirect('salary_list')

def salary_edit(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            general = form.cleaned_data['General']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC EditSalary @SalaryId=%s, @General=%s", [pk, general])
            except Exception as e:
                # Обработка ошибки, если что-то пошло не так
                # Например, вывод ошибки или редирект на страницу ошибки
                pass
            return HttpResponseRedirect(reverse('salary_list') + f'?year={salary.Year}&month={salary.Month}')
    else:
        form = SalaryForm(instance=salary)
    return render(request, 'salary_edit.html', {'form': form, 'salary': salary})


# def update_salary_given_status(request, pk):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC UpdateSalaryGivenStatus @SalaryId=%s", [pk])
#
#     return redirect('salary_list')


# def update_salary_given_status(request, pk):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC UpdateSalaryGivenStatus @SalaryId=%s", [pk])
#     except Exception as e:
#         messages.error(request, f'Ошибка при выдачи зарплаты: {e}')
#
#     return redirect('salary_list')
#


def update_salary_given_status(request, pk):

    try:
        with connection.cursor() as cursor:
            cursor.execute("DECLARE @Result INT; EXEC UpdateSalaryGivenStatus @SalaryId=%s, @Result=@Result OUTPUT; SELECT @Result;", [pk])
            result = cursor.fetchone()[0]
            if result == 1:
                messages.success(request, 'Зарплата успешно выдана')
            elif result == 0:
                messages.error(request, 'Ошибка: Зарплата уже была выдана')
            elif result == -1:
                messages.error(request, 'Ошибка: Недостаточно средств в бюджете')
            else:
                messages.error(request, 'Ошибка: Не удалось выполнить операцию')
    except Exception as e:
        messages.error(request, 'Ошибка: успешно')

    return redirect('salary_list')

# def issue_unissued_salaries(request):
#     if request.method == 'POST':
#         year_str = request.POST.get('year')
#         month_str = request.POST.get('month')
#         print('atest')
#         print(year_str, month_str)
#         if year_str and month_str:  # Проверка на пустые значения
#             try:
#                 year = int(year_str)
#                 month = int(month_str)
#                 print('atest')
#                 print(year, month)
#                 with connection.cursor() as cursor:
#                     cursor.execute("DECLARE @Result INT; EXEC IssueUnissuedSalaries @Year=%s, @Month=%s, @Result=@Result OUTPUT; SELECT @Result;", [year, month])
#                     result = cursor.fetchone()[0]
#                     if result == 1:
#                         messages.success(request, 'Зарплаты успешно выданы')
#                     elif result == 0:
#                         messages.error(request, 'Ошибка: Не удалось выполнить операцию')
#                     elif result == -1:
#                         messages.error(request, 'Ошибка: Не удалось получить информацию о зарплатах за указанный период')
#                     elif result == -2:
#                         messages.error(request, 'Ошибка: Недостаточно средств в бюджете для выдачи зарплат')
#                     else:
#                         messages.error(request, 'Ошибка: Неизвестная ошибка')
#             except Exception as e:
#                 messages.error(request, f'')
#         else:
#             messages.error(request, 'Ошибка: Не выбран год или месяц')
#
#     return redirect('salary_list')


def issue_unissued_salaries(request):
    if request.method == 'POST':
        year_str = request.POST.get('year')
        month_str = request.POST.get('month')
        print('atest')
        if year_str and month_str:
            try:
                year = int(year_str)
                month = int(month_str)
                print('atest')
                print(year, month)
                with connection.cursor() as cursor:
                    cursor.execute("DECLARE @Result INT; EXEC IssueUnissuedSalaries @Year=%s, @Month=%s, @Result=@Result OUTPUT; SELECT @Result;", [year, month])
                    result = cursor.fetchone()[0]
                    if result == 1:
                        messages.success(request, 'Зарплаты успешно выданы')
                    elif result == 0:
                        messages.error(request, 'Ошибка: Не удалось выполнить операцию')
                    elif result == -1:
                        messages.error(request, 'Ошибка: Не удалось получить информацию о зарплатах за указанный период')
                    elif result == -2:
                        messages.error(request, 'Ошибка: Недостаточно средств в бюджете для выдачи зарплат')
                    else:
                        messages.error(request, 'Ошибка: Неизвестная ошибка')
                    print('atest')
                    print(result)
            except Exception as e:
                messages.error(request, f'Успешно')
        else:
            messages.error(request, 'Ошибка: Не выбран год или месяц')

        return HttpResponseRedirect(reverse('salary_list') + f'?year={year_str}&month={month_str}')



