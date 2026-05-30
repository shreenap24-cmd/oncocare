from django import forms
from .models import Treatment

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['treatment_name', 'treatment_type', 'doctor_name',
                  'hospital_name', 'start_date', 'end_date',
                  'total_cycles', 'cycles_completed', 'status', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'type': 'date'}),
        }