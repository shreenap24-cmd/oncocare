
# Create your models here.
from django.db import models
from accounts.models import PatientProfile

class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Once a day'),
        ('twice', 'Twice a day'),
        ('thrice', 'Three times a day'),
        ('weekly', 'Weekly'),
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    reminder_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.medicine_name