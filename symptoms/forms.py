from django import forms
from .models import Symptom

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['symptom_name', 'severity', 'symptom_date', 'notes']
        widgets = {
            'symptom_date': forms.DateInput(attrs={'type': 'date'}),
        }