from django.urls import path
from . import views

app_name = "department"

urlpatterns = [
    path("list/", views.department_list, name="department_list"),
    path("create/", views.create_department, name="create_department"),
    path("<uuid:department_id>/", views.department_detail, name="department_detail"),
    path("<uuid:patient_id>/admit-patient/", views.admit_patient, name="admit_patient"),
    path(
        "<uuid:hospitalization_id>/hospitalization/",
        views.hospitalization_detail,
        name="hospitalization",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/hospitalization-edit/",
        views.edit_patient_symptoms,
        name="hospitalization_update",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/transfer/",
        views.transfer_patient,
        name="transfer",
    ),
    path(
        "<uuid:hospitalization_id>/discharge/",
        views.discharge_patient,
        name="discharge",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/patient-consultation-add/",
        views.create_patient_consultation,
        name="consultation_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/patient-consultation-edit/<uuid:consultation_id>/",
        views.update_patient_consultation,
        name="consultation_update",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/patient-observation-add/",
        views.create_patient_observation,
        name="observation_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/patient-observation-edit/<uuid:observation_id>/",
        views.update_patient_observation,
        name="observation_update",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/vital-signs-add/",
        views.create_vital_signs,
        name="vitals_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/vital-signs-edit/<uuid:vital_id>/",
        views.update_vital_signs,
        name="vitals_update",
    ),
]
