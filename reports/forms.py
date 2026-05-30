from django import forms
from .models import LabReport

class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ['report_title', 'report_file', 'report_date', 'report_summary']
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
        }