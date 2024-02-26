from django.contrib import admin
from django.urls import path, include
from scales.views import access_denied

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("department/", include("department.urls")),
    path("patient/", include("patient.urls")),
    path("scale/", include("scales.urls")),
    path("access-denied/", access_denied, name="access_denied"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)