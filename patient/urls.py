from django.urls import path
from . import views

app_name = "patient"

urlpatterns = [
    path("", views.index, name="index"),
    path("patient/<uuid:pk>/detail/", views.patient_detail, name="detail"),
    path("patient/<uuid:pk>/patient-page/", views.patient_page, name="page"),
    path("patient/<uuid:pk>/patient-observation-add/", views.add_patient_observation, name="observation_add"),
    path("patient/<uuid:patient_id>/patient-observation-edit/<uuid:observation_id>/", views.edit_patient_observation, name="observation_edit"),
    path("patient/add/", views.PatientCreateView.as_view(), name="add"),
    path("patient/<uuid:pk>/update/", views.PatientUpdateView.as_view(), name="update"),
    path("patient/<uuid:pk>/delete/", views.PatientDeleteView.as_view(), name="delete"),
]