from django import forms
from .models import Department, Observation, Hospitalization
from ckeditor.widgets import CKEditorWidget

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
    
class DischargeFrom(forms.Form):
    discharge_date = forms.DateTimeField(
        label="Discharge Date",
        widget=forms.TextInput(attrs={"type": "datetime-local"})
    )