import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from main.models import User
from department.models import Hospitalization

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

PAIN_CHOICES = [
    ("0", 0),
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
    ("10", 10),
]

# Global variables for NEWS 
YES = True
NO = False
YES_NO_CHOICES = [
    (YES, "Yes"),
    (NO, "No"),
]
LOC_CHOICES = [
    ("awake", "Awake"),
    ("verbal", "Patient responds to a verbal stimulus"),
    ("pain", "Patient responds to a pain stimulus"),
    ("unresponsive", "Patient is unresponsive to stimulus")
]

class BodyMassIndex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    body_height = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    body_weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(400)])
    bmi = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    interpretation = models.CharField(max_length=50)
    
    class Meta:
        ordering = ("-created_at",)
        
    def __str__(self):
        return f"{self.hospitalization.patient.first_name} {self.bmi}-points: {self.intepretation}"
    
    def calculate_bmi(self):
        body_height = self.body_height / 100
        bmi = round((self.body_weight / (body_height **2)),1)
        return bmi
    
    def interpretation(self):
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi <= 24.9:
            return "Normal weight"
        elif 25 <= self.bmi <= 29.9:
            return "Overweight"
        elif 30 <= self.bmi <= 34.9:
            return "Obesity class I"
        elif 35 <= self.bmi <= 39.9:
            return "Obesity class II"
        elif self.bmi <= 40:
            return "Obesity class III"
        else:
            return "Error"
        
    def save(self, *args, **kwargs):
        self.bmi = self.calculate_bmi()
        self.interpretation = self.interpretation()
        super().save(*args, **kwargs)
        
        
    
class NortonScale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
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
        return f"{self.hospitalization.patient.first_name} points {self.total_points}"
    
    
        
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
        if self.total_points in [19,20]:
            risk = "Low Risk"
        elif  14 <= self.total_points <= 18:
            risk = "Medium Risk"
        elif 10 <= self.total_points <= 13:
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
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
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

class PainScale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    pain_comment = models.CharField(max_length=255, blank=True, null=True)
    pain_level = models.CharField(max_length=2, choices=PAIN_CHOICES)
    pain_intepretation = models.TextField()
    class Meta:
        ordering = ("-created_at",)
        
    def pain_intepretation(self):
        if self.pain_level == 0:
            interpretation = "No Pain"
        elif self.pain_level in [1,2,3]:
            interpretation = "Mild Pain"
        elif self.pain_level in [4,5,6]:
            interpretation = "Moderate Pain"
        else:
            interpretation = "Severe Pain"
        return interpretation
            
    def save(self, *args, **kwargs):
        self.pain_intepretation = self.pain_intepretation()
        super().save(*args, **kwargs)
        
class NewsScale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    respiratory_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    oxygen_saturation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_on_oxygen = models.BooleanField(choices=YES_NO_CHOICES, default=NO)
    #AECOPD state - Acute exacebrations of chronic obstructive pulmonary disease
    aecopd_state = models.BooleanField(choices=YES_NO_CHOICES, default=NO)
    temperature = models.DecimalField(max_digits=3, decimal_places=1,validators=[MinValueValidator(0), MaxValueValidator(50)])
    systolic_blood_pressure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    diastolic_blood_pressure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    heart_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    level_of_consciousness = models.CharField(max_length=60,choices=LOC_CHOICES, default="awake")
    total_score = models.IntegerField(blank=True, null=True)
    score_interpretation = models.TextField()
    
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
        print(f"OxySup {total}, {self.calculate_is_on_oxygen_score()}")
        total += self.calculate_temperature_score()
        print(f"Temp {total}, {self.calculate_temperature_score()}")
        total += self.calculate_systolic_blood_pressure_score()
        print(f"SBP {total}, {self.calculate_systolic_blood_pressure_score()}")
        total += self.calculate_heart_rate_score()
        print(f"HR {total}, {self.calculate_heart_rate_score()}")
        total += self.calculate_level_of_consciousness_score()
        print(f"LOC {total}, {self.calculate_level_of_consciousness_score()}")
        return total
    
    def score_interpretation(self):
        if self.total_score <= 4:
            return f"National Early Warning Score (NEWS) = {self.total_score}. Interpretation: This is a low score that suggests clinical monitoring should be continued and the medical professional, usually a registered nurse will decide further if clinical care needs to be updated. Note: This tool should NOT be considered as a substitute for any professional medical service, NOR as a substitute for clinical judgement."
        elif self.total_score in [5,6]:
            return f"National Early Warning Score (NEWS) = {self.total_score}. Interpretation: This is a medium score that suggests the patient should be reviewed by a medical specialist with competencies in acute illness, even with the possibility of referring the patient to the critical care unit at the end of the assessment. Note: This tool should NOT be considered as a substitute for any professional medical service, NOR as a substitute for clinical judgement."
        elif 7 <= self.total_score <=20:
            return f"National Early Warning Score (NEWS) = {self.total_score}. Interpretation: This is a high score (red score) that is indicative of urgent critical care need and the patient should be transferred to the appropriate specialized department for further care. Note: This tool should NOT be considered as a substitute for any professional medical service, NOR as a substitute for clinical judgement." 
    
    def save(self, *args, **kwargs):
        self.total_score = self.calculate_total_score()
        self.score_interpretation = self.score_interpretation()
        super().save(*args, **kwargs)

