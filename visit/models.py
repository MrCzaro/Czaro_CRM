import uuid
from django.db import models
from django.utils import timezone
from main.models import User
from patient.models import Patient

class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    admitted_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    admitted_on = models.DateTimeField(default=timezone.now)
    discharged_on = models.DateTimeField(blank=True, null=True)
    is_discharged = models.BooleanField(default=False)
    main_symptom = models.CharField(max_length=255)
    additional_symptoms = models.CharField(max_length=255, blank=True, null=True)
    consent = models.CharField(max_length=255, blank=True)
    consent_contact_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"Visit for {self.patient.first_name} {self.patient.last_name}"
    
    class Meta:
        ordering = ("-admitted_on",)
        
class Observation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visit = models.ForeignKey(Visit, related_name="observations", on_delete=models.CASCADE)
    observation = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        ordering = ("-created_at",)
        