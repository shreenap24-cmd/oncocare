
# Create your models here.
from django.db import models
from accounts.models import PatientProfile

class Treatment(models.Model):
    TREATMENT_TYPES = [
        ('chemotherapy', 'Chemotherapy'),
        ('radiation', 'Radiation Therapy'),
        ('surgery', 'Surgery'),
        ('immunotherapy', 'Immunotherapy'),
        ('hormone', 'Hormone Therapy'),
        ('targeted', 'Targeted Therapy'),
        ('bone_marrow', 'Bone Marrow Transplant'),
        ('radioactive_iodine', 'Radioactive Iodine'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    treatment_name = models.CharField(max_length=100)
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPES)
    doctor_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    total_cycles = models.IntegerField(null=True, blank=True)
    cycles_completed = models.IntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.treatment_name