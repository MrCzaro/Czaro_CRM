from django import forms
from .models import (
    GlasgowComaScale,
    NortonScale,
    PHYSICAL_CHOICES,
    MENTAL_CHOICES,
    ACTIVITY_CHOICES,
    MOBILITY_CHOICES,
    INCONTINENCE_CHOICES,
    EYE_RESPONSE_CHOICES,
    VERBAL_RESPONSE_CHOICES,
    MOTOR_RESPONSE_CHOICES,
)


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