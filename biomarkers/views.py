import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    CancerType,
    CancerMarker,
    PatientCancerProfile,
    BiomarkerReading
)

from .forms import (
    PatientCancerProfileForm,
    BiomarkerReadingForm
)

from accounts.models import PatientProfile


# ─────────────────────────────────────────────
# Cancer Profiles
# ─────────────────────────────────────────────

@login_required
def cancer_profile_list(request):

    patient = PatientProfile.objects.get(
        user=request.user
    )

    profiles = PatientCancerProfile.objects.filter(
        patient=patient
    )

    return render(
        request,
        'biomarkers/cancer_profile_list.html',
        {
            'profiles': profiles
        }
    )


@login_required
def cancer_profile_add(request):

    patient = PatientProfile.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        form = PatientCancerProfileForm(
            request.POST
        )

        if form.is_valid():

            profile = form.save(
                commit=False
            )

            profile.patient = patient

            profile.save()

            return redirect(
                'cancer_profile_list'
            )

    else:

        form = PatientCancerProfileForm()

    return render(
        request,
        'biomarkers/cancer_profile_form.html',
        {
            'form': form
        }
    )


@login_required
def cancer_profile_delete(request, pk):

    patient = PatientProfile.objects.get(
        user=request.user
    )

    profile = get_object_or_404(
        PatientCancerProfile,
        pk=pk,
        patient=patient
    )

    if request.method == 'POST':

        profile.delete()

        return redirect(
            'cancer_profile_list'
        )

    return render(
        request,
        'biomarkers/cancer_profile_confirm_delete.html',
        {
            'profile': profile
        }
    )


# ─────────────────────────────────────────────
# Biomarker Readings
# ─────────────────────────────────────────────

@login_required
def biomarker_readings(request, profile_pk):

    patient = PatientProfile.objects.get(
        user=request.user
    )

    profile = get_object_or_404(
        PatientCancerProfile,
        pk=profile_pk,
        patient=patient
    )

    readings = BiomarkerReading.objects.filter(
        cancer_profile=profile
    ).order_by('reading_date')

    # Group readings by marker for charts

    markers = CancerMarker.objects.filter(
        cancer_type=profile.cancer_type
    )

    chart_data = []

    for marker in markers:

        marker_readings = readings.filter(
            marker=marker
        )

        chart_data.append({

            'marker_name':
                marker.marker_name,

            'unit':
                marker.unit,

            'guidance_text':
                marker.guidance_text,

            'expected_trend':
                marker.expected_trend,

            'dates': json.dumps(
                [
                    str(r.reading_date)
                    for r in marker_readings
                ]
            ),

            'values': json.dumps(
                [
                    float(r.value)
                    for r in marker_readings
                ]
            ),
        })

    return render(
        request,
        'biomarkers/biomarker_readings.html',
        {
            'profile': profile,
            'readings': readings,
            'markers': markers,
            'chart_data': chart_data,
        }
    )


@login_required
def biomarker_add(request, profile_pk):

    patient = PatientProfile.objects.get(
        user=request.user
    )

    profile = get_object_or_404(
        PatientCancerProfile,
        pk=profile_pk,
        patient=patient
    )

    if request.method == 'POST':

        form = BiomarkerReadingForm(
            request.POST
        )

        # IMPORTANT
        form.fields['marker'].queryset = (
            CancerMarker.objects.filter(
                cancer_type=profile.cancer_type
            )
        )

        if form.is_valid():

            reading = form.save(
                commit=False
            )

            reading.cancer_profile = profile

            reading.save()

            return redirect(
                'biomarker_readings',
                profile_pk=profile.pk
            )

    else:
        form = BiomarkerReadingForm()
        markers = CancerMarker.objects.filter(
            cancer_type=profile.cancer_type
    )
    form.fields['marker'].queryset = markers
    form.fields['marker'].empty_label = "Select a marker"

    return render(
        request,
        'biomarkers/biomarker_form.html',
        {
            'form': form,
            'profile': profile,
        }
    )


@login_required
def biomarker_delete(request, pk):

    reading = get_object_or_404(
        BiomarkerReading,
        pk=pk
    )

    profile_pk = (
        reading.cancer_profile.pk
    )

    if request.method == 'POST':

        reading.delete()

        return redirect(
            'biomarker_readings',
            profile_pk=profile_pk
        )

    return render(
        request,
        'biomarkers/biomarker_confirm_delete.html',
        {
            'reading': reading
        }
    )