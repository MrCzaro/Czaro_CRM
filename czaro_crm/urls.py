from django.contrib import admin
from django.urls import path, include
from scales.views import access_denied

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("department/", include("department.urls")),
    path("patient/", include("patient.urls")),
    path("scale/", include("scales.urls")),
    path("access-denied/", access_denied, name="access_denied"),
]
