import uuid


from django.db import models
from django.utils import timezone
from main.models import User


YES = True
NO = False
YES_NO_CHOICES = [
    (YES, "Yes"),
    (NO, "No"),
]
STATUS_CHOICES = [
    ("admitted","Admitted"),
    ("discharged_home" , "Discharged home"),
    #("transferred_facility" , "Transferred to different medical facility"),
    #("died", "Died"),
]


class Patient(models.Model):
    # Credentials
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    is_insured = models.BooleanField(choices=YES_NO_CHOICES, default=YES)
    insurance = models.CharField(max_length=255)
    # adress
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    # inpatient stay
    admitted_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    admitted_on = models.DateTimeField(default=timezone.now)
    consent = models.CharField(max_length = 255, blank=True)
    consent_contact_number = models.CharField(max_length=15, blank=True)
    
    main_symptom = models.CharField(max_length=255)
    additional_symptoms = models.CharField(max_length=255, blank=True, null=True)
    
   
    discharged_on = models.DateTimeField(blank=True, null=True)
    is_discharged = models.BooleanField(default=False)
    status = models.CharField(max_length=45, choices=STATUS_CHOICES, default="admitted")
    died_on = models.DateTimeField(blank=True, null=True)
    def __str__(self):
       return f"{self.first_name} {self.last_name}"
   
class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    admitted_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    admitted_on = models.DateTimeField(default=timezone.now)
    discharged_on = models.DateTimeField(blank=True, null=True)
    is_discharged = models.BooleanField(default=False)
    status = models.CharField(max_length=45, choices=STATUS_CHOICES, default="admitted")
    main_symptom = models.CharField(max_length=255)
    additional_symptoms = models.CharField(max_length=255, blank=True, null=True)
    consent = models.CharField(max_length=255, blank=True)
    consent_contact_number = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return f"Visit for {self.patient.first_name} {self.patient.last_name}"
   
class PatientObservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # change to visit visit = models.ForeignKey(Visit, related_name="observations", on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, related_name = "observations", on_delete=models.CASCADE)
    observation = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        ordering = ("-created_at",)
        