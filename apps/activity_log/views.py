from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import ActivityLog
from .serializer import ActivityLogSerializer


class ActivityLogReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
