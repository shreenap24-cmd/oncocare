from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm
from accounts.models import PatientProfile

@login_required
def appointment_list(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    appointments = appointments.order_by('appointment_date')
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'status_filter': status_filter,
    })

@login_required
def appointment_add(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, "Appointment added successfully!")
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
def appointment_edit(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, patient=patient)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
def appointment_delete(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, patient=patient)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted.")
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {
        'appointment': appointment
    })

@login_required
def appointment_mark_complete(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, patient=patient)
    if request.method == 'POST':
        appointment.status = 'completed'
        appointment.save()
        messages.success(request, "Appointment marked as completed!")
    return redirect('dashboard')