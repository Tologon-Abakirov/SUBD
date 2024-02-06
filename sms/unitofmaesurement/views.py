from django.shortcuts import render, get_object_or_404, redirect
from .models import Unit
from .forms import UnitForm

def Unitlist(request):
    Unites = Unit.objects.all()
    return render(request, 'Unitlist.html', {'Unites': Unites})

def Unitdetail(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    return render(request, 'Unitdetail.html', {'unit': unit})

def Unitcreate(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save()
            return redirect('Unitdetail', pk=unit.pk)
    else:
        form = UnitForm()
    return render(request, 'Unitform.html', {'form': form})

def Unitedit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=Unit)
        if form.is_valid():
            unit = form.save()
            return redirect('Unitdetail', pk=unit.pk)
    else:
        form = UnitForm(instance=unit)
    return render(request, 'Unitedit.html', {'form': form, 'Unit': unit})

def Unitdelete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return redirect('Unitlist')
