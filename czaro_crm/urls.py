from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("patient/", include("patient.urls")),
    path("scale/", include("scales.urls")),
]
