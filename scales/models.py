import uuid
from django.db import models

from patient.models import User, Patient


PHYSICAL_CHOICES = [
    ("4","Good"),
    ("3", "Fair"),
    ("2", "Poor"),
    ("1", "Very Bad")
]
MENTAL_CHOICES = [
    ("4", "Alert"),
    ("3", "Apathetic"),
    ("2", "Confused"),
    ("1", "Stuporous")
]
ACTIVITY_CHOICES = [
    ("4", "Ambulant"),
    ("3", "Walks with help"),
    ("2", "Chairbound"),
    ("1", "Bedridden"),
]
MOBILITY_CHOICES = [
    ("4", "Full"),
    ("3", "Slightly impared"),
    ("2", "Very limited"),
    ("1", "Immobile"),
]
INCONTINENCE_CHOICES = [
    ("4", "None"),
    ("3", "Occasional"),
    ("2", "Usually urinary"),
    ("1", "Urinary and fecal"),
]

class NortonScale(models.Model):
    id = id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, related_name = "norton", on_delete=models.CASCADE)
    physical_condition = models.CharField(max_length=20, choices=PHYSICAL_CHOICES)
    mental_condition = models.CharField(max_length=20, choices=MENTAL_CHOICES)
    activity = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    mobility = models.CharField(max_length=20, choices=MOBILITY_CHOICES)
    incontinence = models.CharField(max_length=20, choices=INCONTINENCE_CHOICES)
    total_points = models.IntegerField(blank=True, null=True)
    pressure_risk = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        ordering = ("-created_at",)
        
    def __str__(self):
        return f"{self.patient.first_name}"
    
    
        
    def calculate_total_points(self):
        choices_values = {
            "4" : 4,
            "3" : 3,
            "2" : 2,
            "1" : 1,
        }

        total = 0
        total += choices_values.get(self.physical_condition, 0)
        total += choices_values.get(self.mental_condition, 0)
        total += choices_values.get(self.activity, 0)
        total += choices_values.get(self.mobility, 0)
        total += choices_values.get(self.incontinence, 0)

        return total
    
    
    def calculate_risk(self):
        if self.total_points > 18 and self.total_points < 21:
            risk = "Low Risk"
        elif self.total_points > 13 and self.total_points <= 18:
            risk = "Medium Risk"
        elif self.total_points >9<= 13 and self.total_points <= 13:
            risk = "High Risk"
        elif self.total_points < 10:
            risk = "Very High Risk"
        else:
            risk = "Error"
            
        return risk
    
    def save(self, *args, **kwargs):
        self.total_points = self.calculate_total_points()
        self.pressure_risk = self.calculate_risk()
        super().save(*args, **kwargs)