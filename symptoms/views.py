from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Symptom
from .forms import SymptomForm
from accounts.models import PatientProfile

@login_required
def symptom_list(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    symptoms = Symptom.objects.filter(patient=patient)
    date_from = request.GET.get('date_from', '')
    date_to   = request.GET.get('date_to', '')
    if date_from:
        symptoms = symptoms.filter(symptom_date__gte=date_from)
    if date_to:
        symptoms = symptoms.filter(symptom_date__lte=date_to)
    symptoms = symptoms.order_by('-symptom_date')
    return render(request, 'symptoms/symptom_list.html', {
        'symptoms':  symptoms,
        'date_from': date_from,
        'date_to':   date_to,
    })

@login_required
def symptom_add(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.patient = patient
            symptom.save()
            messages.success(request, "Symptom logged successfully!")
            return redirect('symptom_list')
    else:
        form = SymptomForm()
    return render(request, 'symptoms/symptom_form.html', {'form': form})

@login_required
def symptom_edit(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    symptom = get_object_or_404(Symptom, pk=pk, patient=patient)
    if request.method == 'POST':
        form = SymptomForm(request.POST, instance=symptom)
        if form.is_valid():
            form.save()
            messages.success(request, "Symptom updated successfully!")
            return redirect('symptom_list')
    else:
        form = SymptomForm(instance=symptom)
    return render(request, 'symptoms/symptom_form.html', {'form': form})

@login_required
def symptom_delete(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    symptom = get_object_or_404(Symptom, pk=pk, patient=patient)
    if request.method == 'POST':
        symptom.delete()
        messages.success(request, "Symptom deleted.")
        return redirect('symptom_list')
    return render(request, 'symptoms/symptom_confirm_delete.html', {
        'symptom': symptom
    })