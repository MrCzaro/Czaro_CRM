from django.urls import path
from . import views

app_name = "patient"

urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:patient_id>/detail/", views.patient_detail, name="detail"),
    path("add/", views.patient_create, name="create"),
    path("<uuid:patient_id>/update/", views.patient_update, name="update"),
    path("<uuid:patient_id>/delete/", views.patient_delete, name="delete"),
]
