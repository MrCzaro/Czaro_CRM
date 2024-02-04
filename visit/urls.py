from django.urls import path
from . import views

app_name = "visit"

urlpatterns = [
    path("<uuid:patient_id>/visit-add/", views.create_visit, name="create"),
    path("<uuid:patient_id>/visit-edit/<uuid:visit_id>/", views.update_visit, name="update"),
    path("<uuid:patient_id>/visit-detail/<uuid:visit_id>/", views.visit_detail, name="detail"),
    path("<uuid:patient_id>/patient-observation-add/", views.add_patient_observation, name="observation_create"),
    path("<uuid:patient_id>/patient-observation-edit/<uuid:observation_id>/", views.edit_patient_observation, name="observation_update"),
]