from django.urls import path
from . import views

app_name = "scales"

urlpatterns = [
    path("<uuid:pk>/norton-add/", views.add_norton_scale, name="norton_add"),
    path("<uuid:patient_id>/norton-edit/<uuid:norton_id>/", views.edit_norton_scale, name="norton_edit"),
    path("<uuid:pk>/glasgow-add/", views.add_glasgow_scale, name="glasgow_add"),
    path("<uuid:patient_id>/glasgow-edit/<uuid:glasgow_id>/", views.edit_glasgow_scale, name="glasgow_edit"),   
]