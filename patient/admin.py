from django.contrib import admin
from .models import Patient, PatientObservation, Visit

admin.site.register(Patient)
admin.site.register(PatientObservation)
admin.site.register(Visit)