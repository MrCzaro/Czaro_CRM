from django import forms
from django.core.exceptions import ValidationError
from .models import (
    BodyMassIndex,
    GlasgowComaScale,
    NewsScale,
    NortonScale,
    PainScale,
    PHYSICAL_CHOICES,
    MENTAL_CHOICES,
    ACTIVITY_CHOICES,
    MOBILITY_CHOICES,
    INCONTINENCE_CHOICES,
    EYE_RESPONSE_CHOICES,
    VERBAL_RESPONSE_CHOICES,
    MOTOR_RESPONSE_CHOICES,
    LOC_CHOICES,
    YES_NO_CHOICES,
    PAIN_CHOICES,
)

NUMERIC_CLASS = "w-1/4 py-1 px-1 bg-stone-200 rounded-md text-black"


class BodyMassIndexForm(forms.ModelForm):
    class Meta:
        model = BodyMassIndex
        fields = [
            "body_height",
            "body_weight",
        ]
        labels = {
            "body_height" : "Body height in cenimeters",
            "body_weight" : "Body weight in kilograms",
        }
        widgets = {
            "body_height" : forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "body_weight" : forms.NumberInput(attrs={"class": NUMERIC_CLASS})
        }
class GlasgowComaScaleForm(forms.ModelForm):
    eye_response = forms.ChoiceField(
        widget=forms.RadioSelect, choices=EYE_RESPONSE_CHOICES
    )
    verbal_response = forms.ChoiceField(
        widget=forms.RadioSelect, choices=VERBAL_RESPONSE_CHOICES
    )
    motor_response = forms.ChoiceField(
        widget=forms.RadioSelect, choices=MOTOR_RESPONSE_CHOICES
    )
    
    class Meta:
        model = GlasgowComaScale
        fields = [
            "eye_response",
            "verbal_response",
            "motor_response",
        ]
        labels = {
            "eye_response" : "Best eye response",
            "verbal_response" : "Best verbal response",
            "motor_response" : "Best motor response",
        }
        
class NewsScaleForm(forms.ModelForm):
    is_on_oxygen = forms.ChoiceField(
        widget=forms.RadioSelect, choices=YES_NO_CHOICES
    )
    aecopd_state = forms.ChoiceField(
        widget=forms.RadioSelect, choices=YES_NO_CHOICES
    )
    level_of_consciousness = forms.ChoiceField(
        widget=forms.RadioSelect, choices=LOC_CHOICES
    )
    
    def clean(self):
        cleaned_data = super().clean()
        systolic_bp = cleaned_data.get("systolic_blood_pressure")
        diastolic_bp = cleaned_data.get("diastolic_blood_pressure")
        
        if systolic_bp is not None and diastolic_bp is not None:
            if systolic_bp < diastolic_bp:
                raise ValidationError(
                    "Systolic blood pressure must be equal or higher than diastolic blood pressure.",
                    code="invalid_blood_pressure"
                )
    class Meta:
        model = NewsScale
        fields = [
            "respiratory_rate",
            "oxygen_saturation",
            "is_on_oxygen",
            "aecopd_state",
            "temperature",
            "systolic_blood_pressure",
            "diastolic_blood_pressure",
            "heart_rate",
            "level_of_consciousness",
        ]
        labels = {
            "respiratory_rate" : "Respiratory rate",
            "oxygen_saturation" : "Oxygen saturation level",
            "is_on_oxygen" : "Oxygen supplementation",
            "aecopd_state" : "Is the patient in Acute exacebrations of chronic obstructive pulmonary disease state",
            "temperature" : "Body temperature",
            "systolic_blood_pressure" : "Systolic blood presurre",
            "diastolic_blood_pressure" : "Diastolic blood pressure",
            "heart_rate" : "Heart Rate",
            "level_of_consciousness " : "Level of consciousness",
        }
        widgets = {
            "respiratory_rate" : forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "oxygen_saturation" : forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "temperature" : forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "systolic_blood_pressure" : forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "diastolic_blood_pressure" : forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
            "heart_rate" : forms.NumberInput(attrs={"class": NUMERIC_CLASS}),
        }
class NortonScaleForm(forms.ModelForm):
    physical_condition = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PHYSICAL_CHOICES
    )
    mental_condition = forms.ChoiceField(
        widget=forms.RadioSelect, choices=MENTAL_CHOICES
    )
    activity = forms.ChoiceField(widget=forms.RadioSelect, choices=ACTIVITY_CHOICES)
    mobility = forms.ChoiceField(widget=forms.RadioSelect, choices=MOBILITY_CHOICES)
    incontinence = forms.ChoiceField(
        widget=forms.RadioSelect, choices=INCONTINENCE_CHOICES
    )

    class Meta:
        model = NortonScale
        fields = [
            "physical_condition",
            "mental_condition",
            "activity",
            "mobility",
            "incontinence",
        ]

class PainScaleForm(forms.ModelForm):
    pain_level = forms.ChoiceField(
        widget = forms.RadioSelect, choices=PAIN_CHOICES
    )
    pain_comment = forms.CharField(
        widget=forms.Textarea(attrs={"class": "w-80 h-20 bg-stone-100 border border-gray-400 p-4"}),
    )
    class Meta:
        model = PainScale
        fields = [
            "pain_level",
            "pain_comment",
        ]