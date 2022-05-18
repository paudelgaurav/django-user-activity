from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.example.urls")),
    path("logs/", include("apps.activity_log.urls")),
]
