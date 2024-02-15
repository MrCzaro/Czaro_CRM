from django.contrib import admin

from .models import Consultation, Department, Hospitalization, Observation

admin.site.register(Consultation)
admin.site.register(Department)
admin.site.register(Hospitalization)
admin.site.register(Observation)
