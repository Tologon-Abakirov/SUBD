from django.shortcuts import render, get_object_or_404, redirect
from .models import Budget
from .forms import BudgetForm

def list(request):
    positions = Budget.objects.all()
    return render(request, 'budget_list.html', {'positions': positions})

def detail(request, pk):
    position = get_object_or_404(Budget, pk=pk)
    return render(request, 'budget_detail.html', {'position': position})

def create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.save()
            return redirect('budget_detail', pk=position.pk)
    else:
        form = BudgetForm()
    return render(request, 'budget_form.html', {'form': form})

def edit(request, pk):
    position = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=position)
        if form.is_valid():
            position.save()
            return redirect('budget_detail', pk=position.pk)
    else:
        form = BudgetForm(instance=position)
    return render(request, 'budget_edit.html', {'form': form, 'position': position})

def delete(request, pk):
    position = get_object_or_404(Budget, pk=pk)
    position.delete()
    return redirect('budget_list')
