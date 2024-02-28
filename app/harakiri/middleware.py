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
        tid, path = getattr(cls._locals, "request_info", (None, None))
        if tid is None or path is None:
            logger.info("No request info found")
            return
        logger.error(f"Harakiri signal received: {tid=} {path=}")

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest) -> http.response.HttpResponseBase:
        t_id = uuid.uuid4()
        path = request.path
        self._locals.request_info = (t_id, path)
        return self.get_response(request)
