from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Treatment
from .forms import TreatmentForm
from accounts.models import PatientProfile


@login_required
def treatment_list(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    treatments = Treatment.objects.filter(patient=patient).order_by('-start_date')
    return render(request, 'treatments/treatment_list.html', {
        'treatments': treatments,
    })


@login_required
def treatment_add(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.patient = patient
            treatment.save()
            messages.success(request, "Treatment added successfully!")
            return redirect('treatment_list')
    else:
        form = TreatmentForm()
    return render(request, 'treatments/treatment_form.html', {'form': form})


@login_required
def treatment_edit(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    treatment = get_object_or_404(Treatment, pk=pk, patient=patient)
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            form.save()
            messages.success(request, "Treatment updated successfully!")
            return redirect('treatment_list')
    else:
        form = TreatmentForm(instance=treatment)
    return render(request, 'treatments/treatment_form.html', {'form': form})


@login_required
def treatment_delete(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    treatment = get_object_or_404(Treatment, pk=pk, patient=patient)
    if request.method == 'POST':
        treatment.delete()
        messages.success(request, "Treatment deleted.")
        return redirect('treatment_list')
    return render(request, 'treatments/treatment_confirm_delete.html', {
        'treatment': treatment,
    })