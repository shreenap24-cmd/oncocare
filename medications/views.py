from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medication
from .forms import MedicationForm
from accounts.models import PatientProfile

@login_required
def medication_list(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    medications = Medication.objects.filter(patient=patient)
    return render(request, 'medications/medication_list.html', {
        'medications': medications
    })

@login_required
def medication_add(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.patient = patient
            medication.save()
            messages.success(request, "Medication added successfully!")
            return redirect('medication_list')
    else:
        form = MedicationForm()
    return render(request, 'medications/medication_form.html', {'form': form})

@login_required
def medication_edit(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    medication = get_object_or_404(Medication, pk=pk, patient=patient)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, "Medication updated successfully!")
            return redirect('medication_list')
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'medications/medication_form.html', {'form': form})

@login_required
def medication_delete(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    medication = get_object_or_404(Medication, pk=pk, patient=patient)
    if request.method == 'POST':
        medication.delete()
        messages.success(request, "Medication deleted.")
        return redirect('medication_list')
    return render(request, 'medications/medication_confirm_delete.html', {
        'medication': medication
    })