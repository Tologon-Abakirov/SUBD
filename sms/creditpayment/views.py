from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db import connection
from django.contrib import messages
from .models import CreditPayment
from .forms import CreditPaymentForm

def ppayment_list(request):
    total_amount = 0
    credit_payments = CreditPayment.objects.all()

    if request.method == 'POST':
        form = CreditPaymentForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            credit_payments = CreditPayment.objects.filter(payment_date__range=[start_date, end_date])
            total_amount = credit_payments.aggregate(total_amount=Sum('total'))['total_amount'] or 0
    else:
        form = CreditPaymentForm()

    context = {'credit_payments': credit_payments, 'form': form, 'total_amount': total_amount}
    return render(request, 'payment_list.html', context)



from django.db import connection

def update_credit_payments(payment_date, credit_id):
    with connection.cursor() as cursor:
        try:
            # Вызов хранимой процедуры
            cursor.execute("EXEC UpdateCreditPayments @payment_date=%s, @credit_id=%s, @result=0", [payment_date, credit_id])
            # Получение результата (если нужно)
            result = cursor.fetchval()
            # Если нужно обработать результат, сделайте это здесь
            return result
        except Exception as e:
            # Обработка ошибок (если нужно)
            print(f"An error occurred: {e}")


def credit_create(request):
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            loan_amount = form.cleaned_data['loan_amount']
            loan_term_months = form.cleaned_data['term_months']
            annual_interest_rate = form.cleaned_data['annual_interest_rate']
            penalty = form.cleaned_data['penalty']
            date_received = form.cleaned_data['date_received']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC CreateCredit @LoanAmount=%s, @LoanTermMonths=%s, @AnnualInterestRate=%s, @Penalty=%s, @DateReceived=%s",
                                   [loan_amount, loan_term_months, annual_interest_rate, penalty, date_received])
                return redirect('credit_list')
            except Exception as e:
                messages.error(request, f'Ошибка при создании кредита: {e}')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        form = CreditForm()

    return render(request, 'credit_create.html', {'form': form})





def credit_edit(request, credit_id):
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            loan_amount = form.cleaned_data['loan_amount']
            loan_term_months = form.cleaned_data['term_months']
            annual_interest_rate = form.cleaned_data['annual_interest_rate']
            penalty = form.cleaned_data['penalty']
            date_received = form.cleaned_data['date_received']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC EditCredit @CreditID=%s, @LoanAmount=%s, @LoanTermMonths=%s, @AnnualInterestRate=%s, @Penalty=%s, @DateReceived=%s",
                                   [credit_id, loan_amount, loan_term_months, annual_interest_rate, penalty, date_received])
                return redirect('credit_list')
            except Exception as e:
                messages.error(request, f'Ошибка при редактировании кредита: {e}')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        # Если метод запроса не POST, показываем форму редактирования существующего кредита
        credit = Credit.objects.get(pk=credit_id)
        form = CreditForm(instance=credit)

    return render(request, 'credit_edit.html', {'form': form})


def credit_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC DeleteCredit @CreditID=%s", [pk])
        messages.success(request, 'Кредит успешно удален.')
    except Exception as e:
        messages.error(request, f'Ошибка при удалении кредита: {e}')
    return redirect('credit_list')