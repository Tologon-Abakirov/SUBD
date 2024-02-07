from django.shortcuts import render, get_object_or_404, redirect
from .models import RawMaterials
from .forms import RawMaterialsForm

def rawlist(request):
    raws = RawMaterials.objects.all()
    return render(request, 'rawlist.html', {'raws': raws})

def rawdetail(request, pk):
    raw = get_object_or_404(RawMaterials, pk=pk)
    return render(request, 'rawdetail.html', {'raw': raw})

def rawcreate(request):
    if request.method == 'POST':
        form = RawMaterialsForm(request.POST)
        if form.is_valid():
            raw = form.save()
            return redirect('rawlist')
    else:
        form = RawMaterialsForm()
    return render(request, 'rawform.html', {'form': form})

def rawedit(request, pk):
    raw = get_object_or_404(RawMaterials, pk=pk)
    if request.method == 'POST':
        form = RawMaterialsForm(request.POST, instance=raw)
        if form.is_valid():
            raw = form.save()
            return redirect('rawlist')
    else:
        form = RawMaterialsForm(instance=raw)
    return render(request, 'rawedit.html', {'form': form, 'raw': raw})

def rawdelete(request, pk):
    raw = get_object_or_404(RawMaterials, pk=pk)
    raw.delete()
    return redirect('rawlist')
