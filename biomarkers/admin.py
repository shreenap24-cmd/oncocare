

# Register your models here.
from django.contrib import admin
from .models import CancerType, CancerMarker, PatientCancerProfile, BiomarkerReading

admin.site.register(CancerType)
admin.site.register(CancerMarker)
admin.site.register(PatientCancerProfile)
admin.site.register(BiomarkerReading)