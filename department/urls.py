from django.urls import path
from . import views

app_name = "department"

urlpatterns = [
    path('list/', views.department_list, name='department_list'),
    path('create/', views.create_department, name='create_department'),
    path("<uuid:department_id>/", views.department_detail, name="department_detail"),
    path('<uuid:patient_id>/admit-patient/', views.admit_patient, name='admit_patient'),
    path("<uuid:hospitalization_id>/hospitalization/", views.hospitalization_detail, name="hospitalization"),
    # path("<uuid:patient_id>/<uuid:department_id>/transfer/", views.transfer_patient, name="transfer"),
    # path("<uuid:patient_id>/<uuid:department_id>/discharge/", views.discharge_patient, name="discharge"),
    path("<uuid:patient_id>/<uuid:department_id>/patient-observation-add/", views.add_patient_observation, name="observation_create"),
    path("<uuid:patient_id>/<uuid:department_id>/patient-observation-edit/<uuid:observation_id>/", views.edit_patient_observation, name="observation_update"),
]

