import re
import logging

from django.utils import timezone

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .utils import get_client_ip
from .settings import (
    TRACK_AJAX_REQUESTS,
    TRACK_ANONYMOUS_USERS,
    TRACK_IGNORE_STATUS_CODES,
    TRACK_IGNORE_URLS,
    TRACK_IGNORE_USER_AGENTS,
    TRACK_PAGEVIEWS,
    TRACK_QUERY_STRING,
    TRACK_REFERER,
    TRACK_SUPERUSERS,
)

track_ignore_urls = [re.compile(x) for x in TRACK_IGNORE_URLS]
track_ignore_user_agents = [
    re.compile(x, re.IGNORECASE) for x in TRACK_IGNORE_USER_AGENTS
]

log = logging.getLogger(__file__)


class VisitorTrackingMiddleware(MiddlewareMixin):
    def _should_track(self, user, request, response):

        # Do not track if HTTP HttpResponse status_code blacklisted
        if response.status_code in TRACK_IGNORE_STATUS_CODES:
            return False

        # Do not track superusers if set
        if user and user.is_superuser and not TRACK_SUPERUSERS:
            return False

        # Do not track ignored urls
        path = request.path_info.lstrip("/")
        for url in track_ignore_urls:
            if url.match(path):
                return False

        # Do not track ignored user agents
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        for user_agent_pattern in track_ignore_user_agents:
            if user_agent_pattern.match(user_agent):
                return False

        # everything says we should track this hit
        return True

    def _add_pageview(self, visitor, request, view_time):
        referer = None
        query_string = None

        if TRACK_REFERER:
            referer = request.META.get("HTTP_REFERER", None)

        if TRACK_QUERY_STRING:
            query_string = request.META.get("QUERY_STRING")

        pageview = Pageview(
            visitor=visitor,
            url=request.path,
            view_time=view_time,
            method=request.method,
            referer=referer,
            query_string=query_string,
        )
        pageview.save()

    def process_response(self, request, response):
        user = getattr(request, "user", None)

        # make sure this is a response we want to track
        if not self._should_track(user, request, response):
            return response

        # Be conservative with the determining time on site since simply
        # increasing the session timeout could greatly skew results. This
        # is the only time we can guarantee.
        now = timezone.now()

        # update/create the visitor object for this request
        visitor = self._refresh_visitor(user, request, now)

        if TRACK_PAGEVIEWS:
            self._add_pageview(visitor, request, now)

        return response
