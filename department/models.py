from django.db import models
from patient.models import Patient
from visit.models import Visit

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Hospitalization(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admitted_on = models.DateTimeField(auto_now_add=True)
    dicharged_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient} - {self.department}"
    
    class Meta:
        unique_together = ["patient", "visit"]