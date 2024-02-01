from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Patient, PatientObservation, Visit

FORM_CLASS = "w-full my-2 py-2 px-2 rounded-xl bg-zinc-100"


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "contact_number",
            "is_insured",
            "insurance",
            "country",
            "city",
            "street",
            "zip_code",
            "admitted_on",
            "admitted_by",
            "main_symptom",
            "additional_symptoms",
            "consent",
            "consent_contact_number",
            
        ]
        
        labels = {
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "date_of_birth": "Date of Birth:",
            "contact_number": "Telephone number:",
            "is_insured" : "Insured:",
            "insurance" : "Insurance Number",
            "country": "Country:",
            "city": "City:",
            "street": "Street adress:",
            "zip_code": "Zip-code:",
            "admitted_on": "Admitted on:",
            "admitted_by": "Admitted by:",
            "main_symptom": "Main symptom",
            "additional_symptoms": "Additional symptoms",
            "consent" : "Authorized Medical Contact",
            "consent_contact_number" : "Authorized person's contact number"
            
        }
        
        widgets = {
            "first_name" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "last_name" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": FORM_CLASS}), # Figure out a widget for picking date usin JS
            "contact_number" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "is_insured" : forms.Select(attrs={"class": FORM_CLASS}),
            "insurance" : forms.NumberInput(attrs={"class": FORM_CLASS, "placeholder" :  "Please type '0' if no insurance."}),
            "country" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "city" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "street" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "zip_code" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "admitted_on" : forms.DateTimeInput(attrs={"type": "datetime-local","class": FORM_CLASS}), # same as with DOB
            "admitted_by" : forms.Select(attrs={"class": FORM_CLASS}),
            "main_symptom": forms.TextInput(attrs={"class": FORM_CLASS}),
            "additional_symptoms": forms.TextInput(attrs={"class": FORM_CLASS}),
            "consent" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "consent_contact_number" : forms.TextInput(attrs={"class": FORM_CLASS}),
        }
        
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
class PatientObservationForm(forms.ModelForm):
    class Meta:
        model = PatientObservation
        fields = ["observation",]
        labels = {"observation": "Patient observation",}
        
        widgets = {
            "observation" : CKEditorWidget(config_name="default")
        }