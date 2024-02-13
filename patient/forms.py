from django import forms
from .models import Patient

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
        }
        
        widgets = {
            "first_name" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "last_name" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": FORM_CLASS}),
            "contact_number" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "is_insured" : forms.Select(attrs={"class": FORM_CLASS}),
            "insurance" : forms.NumberInput(attrs={"class": FORM_CLASS, "placeholder" :  "Please type '0' if no insurance."}),
            "country" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "city" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "street" : forms.TextInput(attrs={"class": FORM_CLASS}),
            "zip_code" : forms.TextInput(attrs={"class": FORM_CLASS}),
        }
        
