from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LabReport
from .forms import LabReportForm
from accounts.models import PatientProfile

@login_required
def report_list(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    reports = LabReport.objects.filter(patient=patient)
    return render(request, 'reports/report_list.html', {'reports': reports})

@login_required
def report_add(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = LabReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.save()
            messages.success(request, "Lab report uploaded successfully!")
            return redirect('report_list')
    else:
        form = LabReportForm()
    return render(request, 'reports/report_form.html', {'form': form})

@login_required
def report_delete(request, pk):
    patient = get_object_or_404(PatientProfile, user=request.user)
    report = get_object_or_404(LabReport, pk=pk, patient=patient)
    if request.method == 'POST':
        report.delete()
        messages.success(request, "Report deleted.")
        return redirect('report_list')
    return render(request, 'reports/report_confirm_delete.html', {
        'report': report
    })