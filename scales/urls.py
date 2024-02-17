from django.urls import path
from . import views

app_name = "scales"

urlpatterns = [
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/bmi-add/",
        views.create_patient_bmi,
        name="bmi_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/bmi-edit/<uuid:bmi_id>/",
        views.update_patient_bmi,
        name="bmi_update",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/glasgow-add/",
        views.create_glasgow_scale,
        name="glasgow_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/glasgow-edit/<uuid:glasgow_id>/",
        views.update_glasgow_scale,
        name="glasgow_update",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/news-add/",
        views.create_news_scale,
        name="news_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/news-edit/<uuid:news_id>/",
        views.update_news_scale,
        name="news_update",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/norton-add/",
        views.create_norton_scale,
        name="norton_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/norton-edit/<uuid:norton_id>/",
        views.update_norton_scale,
        name="norton_update",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/pain-add/",
        views.create_pain_scale,
        name="pain_create",
    ),
    path(
        "<uuid:patient_id>/<uuid:hospitalization_id>/pain-edit/<uuid:pain_id>/",
        views.update_pain_scale,
        name="pain_update",
    ),
]
