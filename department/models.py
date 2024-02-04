import uuid

from django.db import models

from patient.models import Patient
from main.models import User
from visit.models import Visit

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Hospitalization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admitted_on = models.DateTimeField(auto_now_add=True)
    dicharged_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient} - {self.department}"
    
    class Meta:
        unique_together = ["patient", "visit"]