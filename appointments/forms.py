from django import forms
from .models import Appointment
import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor_name', 'hospital_name', 'appointment_date',
                  'appointment_time', 'purpose', 'status']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_appointment_date(self):
        date   = self.cleaned_data.get('appointment_date')
        status = self.cleaned_data.get('status')
        if date and status == 'upcoming' and date < datetime.date.today():
            raise forms.ValidationError(
                "Appointment date cannot be in the past for upcoming appointments."
            )
        return date