from django.shortcuts import render, get_object_or_404, redirect
from .models import Finishs
from .forms import FinishsForm

def Finishs_list(request):
    raws = Finishs.objects.all()
    return render(request, 'Finishs_list.html', {'Finishs': raws})

def Finishs_detail(request, pk):
    raw = get_object_or_404(Finishs, pk=pk)
    return render(request, 'Finishs_detail.html', {'Finish': raw})

def Finishs_create(request):
    if request.method == 'POST':
        form = FinishsForm(request.POST)
        if form.is_valid():
            raw = form.save()
            return redirect('Finishs_detail', pk=raw.pk)
    else:
        form = FinishsForm()
    return render(request, 'Finishs_form.html', {'form': form})

def Finishs_edit(request, pk):
    raw = get_object_or_404(Finishs, pk=pk)
    if request.method == 'POST':
        form = FinishsForm(request.POST, instance=raw)
        if form.is_valid():
            raw = form.save()
            return redirect('Finishs_detail', pk=raw.pk)
    else:
        form = FinishsForm(instance=raw)
    return render(request, 'Finishs_edit.html', {'form': form, 'Finish': raw})

def Finishs_delete(request, pk):
    raw = get_object_or_404(Finishs, pk=pk)
    raw.delete()
    return redirect('Finishs_list')
