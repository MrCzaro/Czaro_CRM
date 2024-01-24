from django.urls import path
from . import views

app_name = "patient"

urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:pk>/detail/", views.patient_detail, name="detail"),
    path("<uuid:pk>/patient-page/", views.patient_page, name="page"),
    path("<uuid:pk>/patient-observation-add/", views.add_patient_observation, name="observation_add"),
    path("<uuid:patient_id>/patient-observation-edit/<uuid:observation_id>/", views.edit_patient_observation, name="observation_edit"),
    path("add/", views.PatientCreateView.as_view(), name="add"),
    path("<uuid:pk>/update/", views.PatientUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", views.PatientDeleteView.as_view(), name="delete"),
]