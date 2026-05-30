
# Create your models here.
from django.db import models
from accounts.models import PatientProfile

class Symptom(models.Model):
    SEVERITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    symptom_name = models.CharField(max_length=100)
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    symptom_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.symptom_name} - {self.symptom_date}"