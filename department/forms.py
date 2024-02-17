from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError

from .models import Consultation, Department, Hospitalization, Observation, VitalSigns


DEPARTMENT_CLASS = "w-full py-3 px-4 bg-stone-200 rounded-md text-black"
HOSPITALIZATION_CLASS = "w-60 py-1 px-1 m-1 rounded-md bg-zinc-100"
NUMERIC_CLASS = "w-1/4 py-1 px-1 bg-stone-200 rounded-md text-black"


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": DEPARTMENT_CLASS}),
            "description": forms.Textarea(attrs={"class": DEPARTMENT_CLASS}),
        }

    def clean(self):
        cleaned_data = super().clean()
        created_by = self.initial.get("created_by")

        # Check if the user has the admin profession
        if created_by and created_by.profession != "admins":
            raise forms.ValidationError(
                "Only users with the admin profession can create departments."
            )

        return cleaned_data


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ["consultation_name", "consultation"]
        labels = {
            "consultation_name": "Name of Consultation",
            "consultation": "Description",
        }
        widgets = {
            "consultation": CKEditorWidget(config_name="default"),
            "consultation_name": forms.TextInput(
                attrs={"class": "w-full py-1 px-1 bg-stone-200 rounded-md text-black"}
            ),
        }


class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = [
            "observation",
        ]
        labels = {
            "observation": "Patient observation",
        }

        widgets = {"observation": CKEditorWidget(config_name="default")}


class HospitalizationForm(forms.ModelForm):
    department_id = forms.UUIDField(
        widget=forms.HiddenInput()
    )  # Add a hidden field for department_id

    class Meta:
        model = Hospitalization
        fields = ["main_symptom", "additional_symptoms", "department_id"]
        labels = {
            "main_symptom": "Main symptom",
            "additional_symptoms": "Additional symptoms",
        }
        widgets = {
            "main_symptom": forms.TextInput(attrs={"class": HOSPITALIZATION_CLASS}),
            "additional_symptoms": forms.TextInput(
                attrs={"class": HOSPITALIZATION_CLASS}
            ),
        }


class TransferPatientForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        label="Transfer to Department",
    )


class DischargeForm(forms.Form):
    discharge_date = forms.DateField(
        label="Discharge Date", widget=forms.DateInput(attrs={"type": "date"})
    )
    discharge_time = forms.TimeField(
        label="Discharge Time", widget=forms.TimeInput(attrs={"type": "time"})
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
                    code="invalid_blood_pressure",
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
            "respiratory_rate": "Respiratory rate",
            "oxygen_saturation": "Oxygen saturation level",
            "temperature": "Body temperature",
            "systolic_blood_pressure": "Systolic blood presurre",
            "diastolic_blood_pressure": "Diastolic blood pressure",
            "heart_rate": "Heart Rate",
        }
        widgets = {
            "respiratory_rate": forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "oxygen_saturation": forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "temperature": forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "systolic_blood_pressure": forms.NumberInput(
                attrs={"class": NUMERIC_CLASS}
            ),
            "diastolic_blood_pressure": forms.NumberInput(
                attrs={"class": NUMERIC_CLASS}
            ),
            "heart_rate": forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
        }
