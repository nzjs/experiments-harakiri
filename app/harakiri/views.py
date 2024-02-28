import logging
import time

from django.shortcuts import render

logger = logging.getLogger("APP-VIEWS")


def index(request):
    logger.info("REQUEST: index")
    return render(request, "index.html")


def slow(request):
    logger.info("REQUEST: slow")
    time.sleep(15)
    logger.info("REQUEST: wakeup from slow")
    return render(request, "index.html")
