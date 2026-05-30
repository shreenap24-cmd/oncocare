

# Create your models here.
from django.db import models
from accounts.models import PatientProfile

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    def __str__(self):
        return f"{self.doctor_name} - {self.appointment_date}"