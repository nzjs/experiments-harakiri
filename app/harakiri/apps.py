import signal

from django.apps import AppConfig

from harakiri.middleware import HarakiriLoggerMiddleware


class HarakiriConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "harakiri"

    def ready(self) -> None:
        signal.signal(signal.SIGSYS, HarakiriLoggerMiddleware.handle_signal)
        return super().ready()
