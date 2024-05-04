from django.shortcuts import render, redirect
from .models import Credit
from django.db.models import Sum
from django.db import connection
from django.contrib import messages
from .forms import CreditForm
from .forms import PreCreditPaymentForm
from creditpayment.forms import CreditPaymentForm
from .models import PreCreditPayment
from creditpayment.models import CreditPayment
from django.urls import reverse
def credit_list(request):
    total_amount = 0
    credits = Credit.objects.all()

    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            credits = Credit.objects.filter(DateReceived__range=[start_date, end_date])
            total_amount = credits.aggregate(total_amount=Sum('LoanAmount'))['total_amount'] or 0
    else:
        form = CreditForm()

    context = {'credits': credits, 'form': form, 'total_amount': total_amount}
    return render(request, 'credit_list.html', context)




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





def credit_edit(request, pk):
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
                                   [pk, loan_amount, loan_term_months, annual_interest_rate, penalty, date_received])
                return redirect('credit_list')
            except Exception as e:
                messages.error(request, f'Ошибка при редактировании кредита: {e}')
        else:
            messages.error(request, 'Форма содержит ошибки.')
    else:
        # Если метод запроса не POST, показываем форму редактирования существующего кредита
        credit = Credit.objects.get(pk=pk)
        form = CreditForm(instance=credit)

    return render(request, 'credit_edit.html', {'form': form, 'credit': credit})



def credit_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC DeleteCredit @CreditID=%s", [pk])
        messages.success(request, 'Кредит успешно удален.')
    except Exception as e:
        messages.error(request, f'Ошибка при удалении кредита: {e}')
    return redirect('credit_list')







from django.http import JsonResponse
from django.template.loader import render_to_string


from django.http import JsonResponse




def payment_list(request, pk):
    total_amount = 0
    selected_date = None

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
    elif 'selectedDate' in request.COOKIES:
        selected_date = request.COOKIES['selectedDate']

    with connection.cursor() as cursor:
        cursor.execute("EXEC PreUpdateCreditPayments @payment_date=%s, @credit_id=%s", [selected_date, pk])
        # Прочие действия с курсором
        cursor.close()

    credit_payments = PreCreditPayment.objects.all()

    if request.method == 'POST':
        form = PreCreditPaymentForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            credit_payments = PreCreditPayment.objects.filter(payment_date__range=[start_date, end_date])
            total_amount = credit_payments.aggregate(total_amount=Sum('total'))['total_amount'] or 0
    else:
        form = PreCreditPaymentForm()

    context = {'credit_payments': credit_payments, 'form': form, 'total_amount': total_amount}

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        response = render(request, 'credit_paymentnow.html', context)
    else:
        response = render(request, 'credit_paymentnow.html', context)

    if selected_date:
        response.set_cookie('selectedDate', selected_date)

    return response






def update_credit_payments(request, pk):
    total_amount = 0
    selected_date = None
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
    elif 'selectedDate' in request.COOKIES:
        selected_date = request.COOKIES['selectedDate']
    elif 'selected_date' in request.GET:
        selected_date = request.GET.get('selected_date')

    with connection.cursor() as cursor:
        try:
            # Вызов хранимой процедуры
            cursor.execute("DECLARE @Result INT; EXEC UpdateCreditPayments @payment_date=%s, @credit_id=%s, @result=@Result OUTPUT; SELECT @Result;", [selected_date,pk])
            result = cursor.fetchone()[0]
            print("Result:", result)  # Печать значения result
            if result == 1:
                messages.success(request, 'Оплачено')
            elif result == 0:
                messages.error(request, 'Ошибка:Кредит за этот период оплачен')
            elif result == -1:
                messages.error(request, 'Ошибка: Недостаточно средств в бюджете')
            else:
                messages.error(request, 'Ошибка: Не удалось выполнить операцию')
                print("Error:", result)  # Печать значения result в случае ошибки
        except Exception as e:
            # Обработка ошибок (если нужно)
            print(f"An error occurred: {e}")
    return redirect(reverse('credit_paymentnow', kwargs={'pk': pk}) + f'?selected_date={selected_date}')



def ppayment_list(request, pk):
    total_amount = 0
    credit_payments = CreditPayment.objects.filter(credit_id=pk)

    if request.method == 'POST':
        form = CreditPaymentForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            credit_payments = credit_payments.filter(payment_date__range=[start_date, end_date])
            total_amount = credit_payments.aggregate(total_amount=Sum('total'))['total_amount'] or 0
    else:
        form = CreditPaymentForm()

    context = {'credit_payments': credit_payments, 'form': form, 'total_amount': total_amount}
    return render(request, 'payment_list.html', context)
