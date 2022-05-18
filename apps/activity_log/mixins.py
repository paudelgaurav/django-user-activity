import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError

from .models import LogAction
from .constants import READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED


class LogActionMixin:
    """
    Mixin to track user actions

    :cvar custom_log_message:
        Log message to populate remarks in LogAction

        type --> str

        set this value or override get_log_message

        If not set then, default log message is built.
    """

    custom_log_message = None

    def get_action_type(self, request):
        return self.action_type_mapper().get(f"{request.method.upper()}")

    def build_log_message(self, request):
        return f"User: {self._get_user(request)} -- Action Type: {self.get_action_type(request)} Path: {request.resolver_match.url_name}"

    def get_log_message(self, request):
        return self.custom_log_message or self.build_log_message(request)

    @staticmethod
    def action_type_mapper():
        return {
            "GET": READ,
            "POST": CREATE,
            "PUT": UPDATE,
            "PATCH": UPDATE,
            "DELETE": DELETE,
        }

    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated else None

    def write_log(self, request, response):
        status = SUCCESS if response.status_code < 400 else FAILED
        user = self._get_user(request)

        if user and not settings.TESTING:
            logging.info("Started Log Entry")

            data = {
                "user": user,
                "action_type": self.get_action_type(request),
                "status": status,
                "remarks": self.get_log_message(request),
            }
            try:
                data["content_type"] = ContentType.objects.get_for_model(
                    self.get_queryset().model
                )
                data["content_object"] = self.get_object()
            except (AttributeError, ValidationError):
                data["content_type"] = None
            except AssertionError:
                pass

            LogAction.objects.create(**data)

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self.write_log(request, response)

        return response
