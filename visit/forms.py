from django import forms
from ckeditor.widgets import CKEditorWidget

FORM_CLASS = "w-full my-2 py-2 px-2 rounded-xl bg-zinc-100"

from .models import Visit, Observation
from department.models import Department

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            "admitted_on",
            "admitted_by",
            "main_symptom",
            "additional_symptoms",
            "consent",
            "consent_contact_number", 
        ]
               
        labels = {
            "admitted_on": "Admitted on:",
            "admitted_by": "Admitted by:",
            "main_symptom": "Main symptom",
            "additional_symptoms": "Additional symptoms",
            "consent" : "Authorized Medical Contact",
            "consent_contact_number" : "Authorized person's contact number"
            
        }
        
        widgets = {
            "admitted_on" : forms.DateTimeInput(attrs={"type": "datetime-local","class": FORM_CLASS}), # same as with DOB
            "admitted_by" : forms.Select(attrs={"class": FORM_CLASS}),
            "main_symptom": forms.TextInput(attrs={"class": FORM_CLASS}),
            "additional_symptoms": forms.TextInput(attrs={"class": FORM_CLASS}),
            "consent" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "consent_contact_number" : forms.TextInput(attrs={"class": FORM_CLASS}),
            
        }
        
class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ["observation",]
        labels = {"observation": "Patient observation",}
        
        widgets = {
            "observation" : CKEditorWidget(config_name="default")
        }

class AdmitPatientForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'your-custom-class'}))