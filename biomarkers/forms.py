from django import forms
from .models import PatientCancerProfile, BiomarkerReading , CancerMarker

class PatientCancerProfileForm(forms.ModelForm):
    class Meta:
        model = PatientCancerProfile
        fields = ['cancer_type', 'diagnosis_date', 'notes']
        widgets = {
            'diagnosis_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BiomarkerReadingForm(forms.ModelForm):
    class Meta:
        model = BiomarkerReading
        fields = ['marker', 'value', 'reading_date', 'notes']
        widgets = {
            'reading_date': forms.DateInput(attrs={'type': 'date'}),
        }