
# Create your models here.
from django.db import models
from accounts.models import PatientProfile

class CancerType(models.Model):
    cancer_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.cancer_name

class CancerMarker(models.Model):
    TREND_CHOICES = [
        ('decrease', 'Should decrease over time'),
        ('normalize', 'Should normalize to healthy range'),
        ('suppress', 'Should stay suppressed/low'),
    ]
    cancer_type = models.ForeignKey(CancerType, on_delete=models.CASCADE,
                                    related_name='markers')
    marker_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    expected_trend = models.CharField(max_length=20, choices=TREND_CHOICES)
    guidance_text = models.TextField()

    def __str__(self):
        return f"{self.cancer_type} - {self.marker_name}"

class PatientCancerProfile(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE,
                                related_name='cancer_profiles')
    cancer_type = models.ForeignKey(CancerType, on_delete=models.CASCADE)
    diagnosis_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient} - {self.cancer_type}"

class BiomarkerReading(models.Model):
    cancer_profile = models.ForeignKey(PatientCancerProfile,
                                       on_delete=models.CASCADE,
                                       related_name='readings')
    marker = models.ForeignKey(CancerMarker, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    reading_date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['reading_date']

    def __str__(self):
        return f"{self.marker.marker_name}: {self.value} on {self.reading_date}"