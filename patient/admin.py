from django.contrib import admin
from .models import Patient, PatientObservation

admin.site.register(Patient)
admin.site.register(PatientObservation)
