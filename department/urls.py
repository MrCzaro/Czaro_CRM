from django.urls import path
from . import views

app_name = "department"

urlpatterns = [
    path('list/', views.department_list, name='department_list'),
    path('create/', views.create_department, name='create_department'),
    path("<uuid:patient_id>/<uuid:visit_id>/<uuid:department_id>/admit/", views.admit_patient, name="admit"),
    path("<uuid:patient_id>/<uuid:visit_id>/<uuid:department_id>/transfer/", views.transfer_patient, name="transfer"),
    path("<uuid:patient_id>/<uuid:visit_id>/<uuid:department_id>/discharge/", views.discharge_patient, name="discharge"),
]

