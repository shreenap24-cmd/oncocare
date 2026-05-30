from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from appointments.models import Appointment
import datetime

class Command(BaseCommand):
    help = "Sends email reminders for tomorrow's appointments"

    def handle(self, *args, **kwargs):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        appointments = Appointment.objects.filter(
            appointment_date=tomorrow,
            status='upcoming'
        ).select_related('patient__user')

        if not appointments.exists():
            self.stdout.write("No appointments tomorrow. No emails sent.")
            return

        sent = 0
        for appt in appointments:
            user = appt.patient.user
            if not user.email:
                self.stdout.write(f"  ⚠️  No email for {user.username}, skipping.")
                continue

            subject = "Oncocare — Appointment Reminder for Tomorrow"

            message = f"""
Hi {user.first_name or user.username},

This is a friendly reminder from Oncocare that you have an appointment tomorrow.

━━━━━━━━━━━━━━━━━━━━━━━━━━
Doctor    : {appt.doctor_name}
Hospital  : {appt.hospital_name}
Date      : {appt.appointment_date.strftime('%d %B %Y')}
Time      : {appt.appointment_time.strftime('%I:%M %p')}
Purpose   : {appt.purpose or 'Follow-up'}
━━━━━━━━━━━━━━━━━━━━━━━━━━

Please remember to bring:
- Your previous lab reports
- Your current medication list
- Any questions you want to ask your doctor

Take care and stay strong.

— The Oncocare Team
            """

            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Email sent to {user.username} at {user.email}")
            )
            sent += 1

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Done! {sent} reminder(s) sent.")
        )