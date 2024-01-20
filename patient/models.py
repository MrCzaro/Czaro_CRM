from django.db import models

from main.models import User

class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    # adress
    country = models.CharField(max_length=255)
    city = models.CharField(max_lenght=255)
    street = models.CharField(max_lenght=255)
    zip_code = models.CharField(max_length=255)
    # inpatient stay
    admitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    admitted_on = models.DateTimeField(auto_now_add=True)
    discharged_on = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"