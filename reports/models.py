
# Create your models here.
from django.db import models
from accounts.models import PatientProfile

class LabReport(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    report_title = models.CharField(max_length=100)
    report_file = models.FileField(upload_to='reports/')
    report_date = models.DateField()
    report_summary = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_title