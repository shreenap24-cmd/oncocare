from django import forms
from .models import Medication

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['medicine_name', 'dosage', 'frequency',
                  'start_date', 'end_date', 'reminder_time']
        widgets = {
            'start_date':    forms.DateInput(attrs={'type': 'date'}),
            'end_date':      forms.DateInput(attrs={'type': 'date'}),
            'reminder_time': forms.TimeInput(attrs={'type': 'time'}),
        }