from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import PatientProfile
from appointments.models import Appointment
from medications.models import Medication
from treatments.models import Treatment
from symptoms.models import Symptom
from reports.models import LabReport
from biomarkers.models import PatientCancerProfile
import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


@login_required
def appointment_mark_complete(request, pk):
    patient     = get_object_or_404(PatientProfile, user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, patient=patient)
    if request.method == 'POST':
        appointment.status = 'completed'
        appointment.save()
        messages.success(request, "Appointment marked as completed.")
    return redirect('appointment_list')


@login_required
def export_pdf(request):
    patient = PatientProfile.objects.get(user=request.user)
    today   = datetime.date.today()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="oncocare_summary_{today}.pdf"'

    doc = SimpleDocTemplate(
        response, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm
    )

    styles = getSampleStyleSheet()
    story  = []

    TEAL  = colors.HexColor('#0a7c7c')
    NAVY  = colors.HexColor('#0d2b45')
    LIGHT = colors.HexColor('#f0f4f8')
    MUTED = colors.HexColor('#6b8190')
    TEXT  = colors.HexColor('#1a2e3b')

    title_style = ParagraphStyle(
        'title', fontSize=24, textColor=NAVY,
        fontName='Helvetica-Bold', spaceAfter=4, leading=30
    )
    sub_style = ParagraphStyle(
        'sub', fontSize=13, textColor=TEAL,
        fontName='Helvetica', spaceAfter=4, leading=18
    )
    meta_style = ParagraphStyle(
        'meta', fontSize=9, textColor=MUTED,
        fontName='Helvetica', spaceAfter=2, leading=14
    )
    heading_style = ParagraphStyle(
        'heading', fontSize=12, textColor=colors.white,
        fontName='Helvetica-Bold', spaceAfter=0,
        spaceBefore=0, leading=16
    )
    footer_style = ParagraphStyle(
        'footer', fontSize=8, textColor=MUTED,
        fontName='Helvetica-Oblique', leading=12
    )

    # ── HEADER ──────────────────────────────────────
    story.append(Paragraph("Oncocare", title_style))
    story.append(Paragraph("Personal Health Summary", sub_style))
    story.append(Paragraph(
        f"Patient: <b>{patient.user.get_full_name() or patient.user.username}</b>",
        meta_style
    ))
    story.append(Paragraph(
        f"Generated: {today.strftime('%d %B %Y')}",
        meta_style
    ))
    story.append(Spacer(1, 0.4*cm))

    divider = Table([['']], colWidths=[17*cm])
    divider.setStyle(TableStyle([
        ('LINEBELOW',     (0,0), (-1,-1), 2, TEAL),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(divider)
    story.append(Spacer(1, 0.5*cm))

    # ── SECTION HELPER ──────────────────────────────
    def add_section(title, headers, rows, col_widths):
        heading_table = Table(
            [[Paragraph(title, heading_style)]],
            colWidths=[17*cm]
        )
        heading_table.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), NAVY),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ]))
        story.append(heading_table)
        story.append(Spacer(1, 0.1*cm))

        if not rows:
            rows = [['No records found'] + ['' for _ in range(len(headers)-1)]]

        header_para = [
            Paragraph(f'<b>{h}</b>', ParagraphStyle(
                'th', fontSize=8.5, textColor=TEAL,
                fontName='Helvetica-Bold', leading=12
            ))
            for h in headers
        ]
        data_rows = [
            [
                Paragraph(str(cell), ParagraphStyle(
                    'td', fontSize=9, textColor=TEXT,
                    fontName='Helvetica', leading=13
                ))
                for cell in row
            ]
            for row in rows
        ]

        tbl = Table([header_para] + data_rows, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,0),  LIGHT),
            ('TOPPADDING',    (0,0), (-1,0),  7),
            ('BOTTOMPADDING', (0,0), (-1,0),  7),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('RIGHTPADDING',  (0,0), (-1,-1), 8),
            ('TOPPADDING',    (0,1), (-1,-1), 7),
            ('BOTTOMPADDING', (0,1), (-1,-1), 7),
            ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.HexColor('#f9fbfc')]),
            ('LINEBELOW',     (0,0), (-1,0),  1,   TEAL),
            ('LINEBELOW',     (0,1), (-1,-1), 0.4, colors.HexColor('#e8edf2')),
            ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#e8edf2')),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.5*cm))

    # ── APPOINTMENTS ────────────────────────────────
    appts = Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:10]
    add_section(
        "Appointments",
        ['Doctor', 'Hospital', 'Date', 'Status'],
        [[
            a.doctor_name,
            a.hospital_name,
            a.appointment_date.strftime('%d %b %Y'),
            a.status.capitalize(),
        ] for a in appts],
        [4.5*cm, 5.5*cm, 3.5*cm, 3.5*cm]
    )

    # ── MEDICATIONS ─────────────────────────────────
    meds = Medication.objects.filter(patient=patient)
    add_section(
        "Medications",
        ['Medicine', 'Dosage', 'Frequency', 'Started'],
        [[
            m.medicine_name,
            m.dosage,
            m.get_frequency_display(),
            m.start_date.strftime('%d %b %Y'),
        ] for m in meds],
        [5.5*cm, 3*cm, 4.5*cm, 4*cm]
    )

    # ── TREATMENTS ──────────────────────────────────
    txs = Treatment.objects.filter(patient=patient)
    add_section(
        "Treatments",
        ['Treatment', 'Type', 'Doctor', 'Status'],
        [[
            t.treatment_name,
            t.get_treatment_type_display(),
            t.doctor_name,
            t.status.capitalize(),
        ] for t in txs],
        [5*cm, 3.5*cm, 4.5*cm, 4*cm]
    )

    # ── SYMPTOMS ────────────────────────────────────
    syms = Symptom.objects.filter(patient=patient).order_by('-symptom_date')[:10]
    add_section(
        "Recent Symptoms",
        ['Symptom', 'Severity', 'Date'],
        [[
            s.symptom_name,
            f"{s.severity}/10",
            s.symptom_date.strftime('%d %b %Y'),
        ] for s in syms],
        [8*cm, 4*cm, 5*cm]
    )

    # ── FOOTER ──────────────────────────────────────
    footer_divider = Table([['']], colWidths=[17*cm])
    footer_divider.setStyle(TableStyle([
        ('LINEABOVE',     (0,0), (-1,-1), 0.5, colors.HexColor('#e0e0e0')),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(footer_divider)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "This document was generated by Oncocare. "
        "It is for personal reference only and is not a medical report. "
        "Always follow the advice of your doctor.",
        footer_style
    ))

    doc.build(story)
    return response


@login_required
def dashboard_view(request):
    patient = PatientProfile.objects.get(user=request.user)
    today   = datetime.date.today()

    # ── COUNTS ──────────────────────────────────────
    total_appointments = Appointment.objects.filter(patient=patient).count()
    total_medications  = Medication.objects.filter(patient=patient).count()
    total_treatments   = Treatment.objects.filter(patient=patient).count()
    total_symptoms     = Symptom.objects.filter(patient=patient).count()
    total_reports      = LabReport.objects.filter(patient=patient).count()

    # ── NEW USER FLAG ────────────────────────────────
    is_new_user = (
        total_appointments == 0 and
        total_medications  == 0 and
        total_treatments   == 0 and
        total_symptoms     == 0
    )

    # ── UPCOMING APPOINTMENTS ────────────────────────
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        status='upcoming',
        appointment_date__gte=today,
    ).order_by('appointment_date')[:5]

    # ── ACTIVE MEDICATIONS ───────────────────────────
    active_medications = (
        Medication.objects.filter(
            patient=patient,
            start_date__lte=today,
            end_date__gte=today,
        )
        |
        Medication.objects.filter(
            patient=patient,
            end_date__isnull=True,
        )
    )

    # ── ONGOING TREATMENTS ───────────────────────────
    ongoing_treatments = Treatment.objects.filter(
        patient=patient,
        status='ongoing',
    )

    # ── RECENT SYMPTOMS ──────────────────────────────
    recent_symptoms = Symptom.objects.filter(
        patient=patient,
    ).order_by('-symptom_date')[:5]

    # ── CANCER PROFILES ──────────────────────────────
    cancer_profiles = PatientCancerProfile.objects.filter(
        patient=patient,
    ).select_related('cancer_type').prefetch_related('cancer_type__markers')

    # ── CONTEXT ──────────────────────────────────────
    context = {
        'patient':               patient,
        'today':                 today,
        'total_appointments':    total_appointments,
        'total_medications':     total_medications,
        'total_treatments':      total_treatments,
        'total_symptoms':        total_symptoms,
        'total_reports':         total_reports,
        'is_new_user':           is_new_user,
        'upcoming_appointments': upcoming_appointments,
        'active_medications':    active_medications,
        'ongoing_treatments':    ongoing_treatments,
        'recent_symptoms':       recent_symptoms,
        'cancer_profiles':       cancer_profiles,
    }

    return render(request, 'dashboard/dashboard.html', context)