from django.contrib import admin
from .models import ActivityLog


class ActivityLogAdmin(admin.ModelAdmin):
    model = ActivityLog

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


admin.site.register(ActivityLog, ActivityLogAdmin)
