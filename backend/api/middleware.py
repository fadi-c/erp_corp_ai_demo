import logging

logger = logging.getLogger("django.request")

class LogIPMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        logger.info(f"{ip} {request.method} {request.path}")

        return self.get_response(request)