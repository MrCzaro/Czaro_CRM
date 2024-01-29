import uuid
from django.db import models

from patient.models import User, Patient

# Global variables for NortonScale
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

# Global variables for GlasgowComaScale
EYE_RESPONSE_CHOICES =[
    ("4", "Eyes open spontaneously"),
    ("3", "Eye opening to sound"),
    ("2", "Eye opening to pain"),
    ("1", "No eye opening"),
]
VERBAL_RESPONSE_CHOICES = [
    ("5", "Orientated"),
    ("4", "Confused"),
    ("3", "Inappropriate words"),
    ("2", "Incomprehensible sounds"),
    ("1", "No verbal response"),
]
MOTOR_RESPONSE_CHOICES = [
    ("6", "Obeys commands"),
    ("5", "Localizing pain"),
    ("4", "Withdrawal from pain"),
    ("3", "Abnormal flexion to pain"),
    ("2", "Abnormal extension to pain"),
    ("1", "No motor response"),
]

class NortonScale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        
class GlasgowComaScale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, related_name = "glasgow", on_delete=models.CASCADE)
    eye_response = models.CharField(max_length=30, choices=EYE_RESPONSE_CHOICES)
    verbal_response = models.CharField(max_length=30, choices=VERBAL_RESPONSE_CHOICES)
    motor_response = models.CharField(max_length=30, choices=MOTOR_RESPONSE_CHOICES)
    total_points = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ("-created_at",)
        
    def __str__(self):
        return f"{self.patient.first_name}"
    
    
        
    def calculate_total_points(self):
        choices_values = {
            "6" : 6,
            "5" : 5,
            "4" : 4,
            "3" : 3,
            "2" : 2,
            "1" : 1,
        }

        total = 0
        total += choices_values.get(self.eye_response , 0)
        total += choices_values.get(self.verbal_response, 0)
        total += choices_values.get(self.motor_response, 0)

        return total
    
    def save(self, *args, **kwargs):
        self.total_points = self.calculate_total_points()
        super().save(*args, **kwargs)

class NewsScale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, related_name = "news", on_delete=models.CASCADE)
    respiratory_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    oxygen_saturation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_on_oxygen = models.BooleanField(choices=YES_NO_CHOICES, default=NO)
    #AECOPD state - Acute exacebrations of chronic obstructive pulmonary disease
    aecopd_state = models.BooleanField(choices=YES_NO_CHOICES, default=NO)
    temperature = models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0), MaxValueValidator(50)])
    systolic_blood_pressure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    diastolic_blood_pressure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    heart_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    level_of_consciousness = models.CharField(max_length=60,choices=LOC_CHOICES, default="awake")
    total_score = models.IntegerField(blank=True, null=True)
    score_interpretation = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ("-created_at",)
        
    def __str__(self):
        return f"{self.aecopd_state} {self.respiratory_rate} {self.level_of_consciousness} {self.heart_rate}"
    
    def calculate_respiratory_respiratory_rate_score(self):
        if self.respiratory_rate <= 8:
            return 3
        elif 9 <= self.respiratory_rate <= 11:
            return 1
        elif 12 <= self.respiratory_rate <= 20:
            return 0
        elif 21 <= self.respiratory_rate <= 24:
            return 2
        else:
            return 3
    
    def calculate_oxygen_saturation_score(self):
        if self.aecopd_state:
            if self.oxygen_saturation  <= 83:
                return 3
            elif self.oxygen_saturation in [84, 85]:
                return 2
            elif self.oxygen_saturation  in [86, 87]:
                return 1
            elif (88 <= self.oxygen_saturation <= 92) or (93 <= self.oxygen_saturation and not self.is_on_oxygen):
                return 0
            elif self.is_on_oxygen:
                if self.oxygen_saturation  in [93, 94]:
                    return 1
                elif self.oxygen_saturation  in [95, 96]:
                    return 2
                elif self.oxygen_saturation  >= 97:
                    return 3
        elif not self.aecopd_state:
            if self.oxygen_saturation <= 91:
                return 3
            elif self.oxygen_saturation in [92, 93]:
                return 2
            elif self.oxygen_saturation in [94, 95]:
                return 1
            elif self.oxygen_saturation >= 96:
                return 0
            
    def calculate_is_on_oxygen_score(self):
        if self.is_on_oxygen:
            return 2
        elif not self.is_on_oxygen:
            return 0
        
    def calculate_temperature_score(self):
        if self.temperature <= 35.0:
            return 3
        elif 35.1 <= self.temperature <= 36.0:
            return 1
        elif 36.1 <= self.temperature <= 38.0:
            return 0
        elif 38.1 <= self.temperature <= 39.0:
            return 1
        elif self.temperature >= 39.1:
            return 2
        
    def calculate_systolic_blood_pressure_score(self):
        if self.systolic_blood_pressure <= 90:
            return 3
        elif 91 <= self.systolic_blood_pressure <= 100:
            return 2
        elif 101 <= self.systolic_blood_pressure <= 110:
            return 1
        elif 111 <= self.systolic_blood_pressure <= 219:
            return 0
        elif self.systolic_blood_pressure >= 220:
            return 3
        
    def calculate_heart_rate_score(self):
        if self.heart_rate <= 40:
            return 3
        elif 40 <= self.heart_rate <= 50:
            return 1
        elif 51 <= self.heart_rate <= 90:
            return 0
        elif 91 <= self.heart_rate <= 110:
            return 1
        elif 111 <= self.heart_rate <= 130:
            return 2
        elif self.heart_rate > 131:
            return 3
        
    def calculate_level_of_consciousness_score(self):
        if self.level_of_consciousness == "awake":
            return 0 
        elif self.level_of_consciousness in ["verbal", "pain", "unresponsive"]:
            return 3
    
    def calculate_total_score(self):
        total = 0
        total += self.calculate_respiratory_respiratory_rate_score()
        print(f"RR {total}, {self.calculate_respiratory_respiratory_rate_score()}")
        total += self.calculate_oxygen_saturation_score()
        print(f"Oxy {total}, {self.calculate_oxygen_saturation_score()}")
        total += self.calculate_is_on_oxygen_score()
        print(f"Oxysup {total}, {self.calculate_is_on_oxygen_score()}")
        total += self.calculate_temperature_score()
        print(f"temp {total}, {self.calculate_temperature_score()}")
        total += self.calculate_systolic_blood_pressure_score()
        print(f"sbp {total}, {self.calculate_systolic_blood_pressure_score()}")
        total += self.calculate_heart_rate_score()
        print(f"hr {total}, {self.calculate_heart_rate_score()}")
        total += self.calculate_level_of_consciousness_score()
        print(f"loc {total}, {self.calculate_level_of_consciousness_score()}")
        return total
    
    def save(self, *args, **kwargs):
        self.total_score = self.calculate_total_score()
        super().save(*args, **kwargs)