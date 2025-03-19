from decouple import config
from django.conf import settings

from rest_framework.throttling import SimpleRateThrottle


from application.enums.throttle.enums import ThrottleScopes
from infrastructure.services.ip import IPService


class CustomRateThrottle(SimpleRateThrottle):

    scope_attr = "throttle_scope"

    def __init__(self):
        # Override the usual SimpleRateThrottle, because we can't determine
        # the rate until called by the view.
        pass

    def allow_request(self, request, view):
        # We can only determine the scope once we're called by the view.
        self.scope = getattr(view, self.scope_attr, None)
        IP_service = IPService()
        ip = IP_service.get_client_ip(request)

        if ip in settings.IP_WHITELIST:
            return True

        # Determine the allowed request rate as we normally would during
        # the `__init__` call.

        match self.scope:
            case ThrottleScopes.Crucial.value:
                self.rate = "10/hour"
            case ThrottleScopes.High.value:
                self.rate = "20/minute"
            case ThrottleScopes.Medium.value:
                self.rate = "25/minute"
            case _:  # Default Rate without Scope (Low)
                self.rate = "35/minute"

        if config("TEST_ENV", cast=bool, default=False):
            self.rate = "1000/hour"

        self.num_requests, self.duration = self.parse_rate(self.rate)

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            # self.create_rate_limit_instance(request)
            return self.throttle_failure()
        return self.throttle_success()

    def get_cache_key(self, request, view):
        """
        If `view.throttle_scope` is not set, don't apply this throttle.

        Otherwise generate the unique cache key by concatenating the user id
        with the `.throttle_scope` property of the view.
        """
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}

    # @staticmethod
    # def create_rate_limit_instance(request):
    #     handler = RateLimitHandler()
    #     IP_service = IPService()
    #     data = {
    #         "user_id": (
    #             str(request.user.id) if request.user and request.user.id else None
    #         ),
    #         "user_agent": request.META.get("HTTP_USER_AGENT"),
    #         "session_key": request.session.session_key,
    #         "path": request.path,
    #         "ip": IP_service.get_client_ip(request),
    #     }
    #     handler.create(data)
