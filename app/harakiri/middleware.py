import logging
import uuid
from collections.abc import Callable
from threading import local
from django import http

logger = logging.getLogger("APP-MIDDLEWARE")


class HarakiriLoggerMiddleware:
    _locals = local()

    @classmethod
    def handle_signal(cls, *args: object) -> None:
        """
        Handle the SIGHUP (=1) signal sent by uWSGI when it's about to kill the process.
        This allows us to log the request details before we see a harakiri event.
        """
        tid, request = getattr(cls._locals, "request_info", (None, None))
        if tid is None or request is None:
            logger.info("No request info found")
            return

        # Log the request before the process encounters a graceful shutdown.
        cls._log_harakiri_event(request)

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest) -> http.response.HttpResponseBase:
        t_id = uuid.uuid4()
        self._locals.request_info = (t_id, request)

        import signal

        logger.info(f"signal handlers: {signal.getsignal(signal.SIGHUP)}")

        return self.get_response(request)

    def _log_harakiri_event(self, request: http.HttpRequest) -> None:
        """
        Attempt to log the request before the process is gracefully killed.
        """
        logger.error(f"Harakiri signal received: {request.path=}")
        logger.error("Logging here before graceful shutdown...")

        # TODO: Set up instrumentation to log the request to Datadog. This is a placeholder.
        # The below code is just an example of how we might log the request to DD.

        # import ddtrace
        # from ddtrace import constants as ddtrace_constants
        # from ddtrace.contrib.django import utils as ddtrace_django_utils
        # from django import http

        # root_span = ddtrace.tracer.current_root_span()
        # if root_span is not None:
        #     root_span.error = 1
        #     root_span.set_tag_str(ddtrace_constants.ERROR_MSG, "uWSGI graceful shutdown")
        #     root_span.set_tag_str(ddtrace_constants.ERROR_TYPE, "uWSGI timeout")

        #     ddtrace_django_utils._after_request_tags(
        #         # Pin isn't used in `_after_request_tags` so we don't pass one. Am not sure how to
        #         # load/find the appropriate pin object anyhow.
        #         pin=None,
        #         span=root_span,
        #         request=request,
        #         # This response won't actually be returned by the application, but this is what a
        #         # reverse proxy like Nginx will return if the application doesn't respond in time,
        #         # which is the typical behaviour when uWSGI kills the process.
        #         response=http.HttpResponse(status=504),
        #     )

        # current_span = ddtrace.tracer.current_span()
        # if current_span is not None:
        #     current_span.finish_with_ancestors()
