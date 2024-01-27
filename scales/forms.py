from django import forms
from .models import NortonScale, PHYSICAL_CHOICES, MENTAL_CHOICES, ACTIVITY_CHOICES, MOBILITY_CHOICES, INCONTINENCE_CHOICES


class NortonScaleForm(forms.ModelForm):
    physical_condition = forms.ChoiceField(widget=forms.RadioSelect, choices=PHYSICAL_CHOICES)
    mental_condition = forms.ChoiceField(widget=forms.RadioSelect, choices=MENTAL_CHOICES)
    activity = forms.ChoiceField(widget=forms.RadioSelect, choices=ACTIVITY_CHOICES)
    mobility = forms.ChoiceField(widget=forms.RadioSelect, choices=MOBILITY_CHOICES)
    incontinence = forms.ChoiceField(widget=forms.RadioSelect, choices=INCONTINENCE_CHOICES)

    class Meta:
        model = NortonScale
        fields = [
            "physical_condition",
            "mental_condition",
            "activity",
            "mobility",
            "incontinence",
        ]