from django import forms
from .models import Patient


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
            "is_insured": "Insured:",
            "insurance": "Insurance Number:",
            "country": "Country:",
            "city": "City:",
            "street": "Street adress:",
            "zip_code": "Zip-code:",
        }

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "patient-form"}),
            "last_name": forms.TextInput(attrs={"class": "patient-form"}),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "patient-form"}
            ),
            "contact_number": forms.TextInput(attrs={"class": "patient-form"}),
            "is_insured": forms.Select(attrs={"class": "patient-form"}),
            "insurance": forms.NumberInput(
                attrs={
                    "class": "patient-form",
                    "placeholder": "Please type '0' if no insurance.",
                }
            ),
            "country": forms.TextInput(attrs={"class": "patient-form"}),
            "city": forms.TextInput(attrs={"class": "patient-form"}),
            "street": forms.TextInput(attrs={"class": "patient-form"}),
            "zip_code": forms.TextInput(attrs={"class": "patient-form"}),
        }
