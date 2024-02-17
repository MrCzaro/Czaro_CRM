from django.urls import path
from . import views

app_name = "patient"

urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:patient_id>/detail/", views.patient_detail, name="detail"),
    path("add/", views.patient_create, name="create"),
    path("<uuid:pk>/update/", views.PatientUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", views.PatientDeleteView.as_view(), name="delete"),
]
