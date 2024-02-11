from django import forms
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget

from .models import Consultation, Department, Hospitalization, Observation, VitalSigns


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]
        
        def clean(self):
            cleaned_data = super().clean()
            created_by = self.initial.get('created_by')
            
            # Check if the user has the admin profession
            if created_by and created_by.profession != 'admins':
                raise forms.ValidationError("Only users with the admin profession can create departments.")
            
            return cleaned_data
        
class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ["consultation_name","consultation"]
        labels = {
            "consultation_name" : "Name of Consultation",
            "consultation" : "Description",
        }
        widgets = {
            "consultation" : CKEditorWidget(config_name="default")
        }
        
class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ["observation",]
        labels = {"observation": "Patient observation",}
        
        widgets = {
            "observation" : CKEditorWidget(config_name="default")
        }

class HospitalizationForm(forms.ModelForm):
    department_id = forms.UUIDField(widget=forms.HiddenInput())  # Add a hidden field for department_id

    class Meta:
        model = Hospitalization
        fields = ['main_symptom', 'additional_symptoms']
        
class TransferPatientForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        label = "Transfer to Department"
    )
    
class DischargeForm(forms.Form):
    discharge_date = forms.DateField(
        label="Discharge Date",
        widget=forms.DateInput(attrs={"type": "date"})
    )
    discharge_time = forms.TimeField(
        label="Discharge Time",
        widget=forms.TimeInput(attrs={"type": "time"})
    )

class VitalSignsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        systolic_bp = cleaned_data.get("systolic_blood_pressure")
        diastolic_bp = cleaned_data.get("diastolic_blood_pressure")
        
        if systolic_bp is not None and diastolic_bp is not None:
            if systolic_bp < diastolic_bp:
                raise ValidationError(
                    "Systolic blood pressure must be equal or higher than diastolic blood pressure.",
                    code='invalid_blood_pressure'
                )
    
    class Meta:
        model = VitalSigns
        fields = [
            "respiratory_rate",
            "oxygen_saturation",
            "temperature",
            "systolic_blood_pressure",
            "diastolic_blood_pressure",
            "heart_rate",
        ]
        labels = {
            "respiratory_rate" : "Respiratory rate",
            "oxygen_saturation" : "Oxygen saturation level",
            "temperature" : "Body temperature",
            "systolic_blood_pressure" : "Systolic blood presurre",
            "diastolic_blood_pressure" : "Diastolic blood pressure",
            "heart_rate" : "Heart Rate",
        }