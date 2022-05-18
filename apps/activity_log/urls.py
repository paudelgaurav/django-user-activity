from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ActivityLogReadOnlyViewSet

router = DefaultRouter()


router.register(r"", ActivityLogReadOnlyViewSet, basename="log")

urlpatterns = router.urls
