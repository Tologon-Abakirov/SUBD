from django.shortcuts import render, get_object_or_404, redirect
from .models import Finishs
from .forms import FinishsForm
from django.db import connection
from django.contrib import messages
def Finishs_list(request):
    raws = Finishs.objects.all()
    return render(request, 'Finishs_list.html', {'Finishs': raws})

def Finishs_detail(request, pk):
    raw = get_object_or_404(Finishs, pk=pk)
    return render(request, 'Finishs_detail.html', {'Finish': raw})

# def Finishs_create(request):
#     if request.method == 'POST':
#         form = FinishsForm(request.POST)
#         if form.is_valid():
#             raw = form.save()
#             return redirect('Finishs_list')
#     else:
#         form = FinishsForm()
#     return render(request, 'Finishs_form.html', {'form': form})
#
# def Finishs_edit(request, pk):
#     raw = get_object_or_404(Finishs, pk=pk)
#     if request.method == 'POST':
#         form = FinishsForm(request.POST, instance=raw)
#         if form.is_valid():
#             raw = form.save()
#             return redirect('Finishs_list')
#     else:
#         form = FinishsForm(instance=raw)
#     return render(request, 'Finishs_edit.html', {'form': form, 'Finish': raw})
#
# def Finishs_delete(request, pk):
#     raw = get_object_or_404(Finishs, pk=pk)
#     raw.delete()
#     return redirect('Finishs_list')







def Finishs_create(request):
    if request.method == 'POST':
        form = FinishsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            unit_id = form.cleaned_data['Unit_of_measurement_id'].id
            quantity = form.cleaned_data['Quantity']
            amount = form.cleaned_data['Amount']
            with connection.cursor() as cursor:
                cursor.execute("EXEC CreateFinishs @Name=%s, @UnitID=%s, @Quantity=%s, @Amount=%s", [name, unit_id, quantity, amount])
            return redirect('Finishs_list')
    else:
        form = FinishsForm()
    return render(request, 'Finishs_form.html', {'form': form})

def Finishs_edit(request, pk):
    finish = get_object_or_404(Finishs, pk=pk)
    if request.method == 'POST':
        form = FinishsForm(request.POST, instance=finish)
        if form.is_valid():
            name = form.cleaned_data['Name']
            unit_id = form.cleaned_data['Unit_of_measurement_id'].id
            quantity = form.cleaned_data['Quantity']
            amount = form.cleaned_data['Amount']
            with connection.cursor() as cursor:
                cursor.execute("EXEC EditFinishs @FinishsID=%s, @Name=%s, @UnitID=%s, @Quantity=%s, @Amount=%s", [pk, name, unit_id, quantity, amount])
            return redirect('Finishs_list')
    else:
        form = FinishsForm(instance=finish)
    return render(request, 'Finishs_edit.html', {'form': form, 'Finish': finish})

def Finishs_delete(request, pk):
    finishs = get_object_or_404(Finishs, pk=pk)

    with connection.cursor() as cursor:
        try:
            cursor.execute("EXEC DeleteFinishs @ID=%s", [pk])  # Передаем pk в запрос
            return redirect('Finishs_list')
        except Exception as e:
            messages.error(request, f'Ошибка удаления записи: {e}')
            return redirect('Finishs_list')

