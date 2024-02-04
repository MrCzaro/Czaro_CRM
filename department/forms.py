from django import forms
from .models import Department

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