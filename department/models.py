import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from patient.models import Patient
from main.models import User


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
    patient = models.ForeignKey(Patient, related_name="hospitalizations",on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admitted_on = models.DateTimeField(auto_now_add=True)
    dicharged_on = models.DateTimeField(null=True, blank=True)
    is_discharged = models.BooleanField(default=False)
    main_symptom = models.CharField(max_length=255)
    additional_symptoms = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient} - {self.department}"
    
    class Meta:
        ordering = ("-admitted_on",)

class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    consultation_name = models.CharField(max_length=255)
    consultation = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.created_by} - {self.created_at}"
    
    class Meta:
        ordering = ("-created_at",)

class Observation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    observation = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.created_by} - {self.created_at}"
    
    class Meta:
        ordering = ("-created_at",)
        
class VitalSigns(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    systolic_blood_pressure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    diastolic_blood_pressure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    respiratory_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    oxygen_saturation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    temperature = models.DecimalField(max_digits=3, decimal_places=1,validators=[MinValueValidator(0), MaxValueValidator(50)])
    heart_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    
    def __str__(self):
        return f"{self.created_by} - {self.created_at}"
    
    class Meta:
        ordering = ("-created_at",)