from django.conf import settings


class SecurityHeadersMiddleware:
    """Añade Content-Security-Policy y Permissions-Policy a todas las respuestas."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp = getattr(settings, "CONTENT_SECURITY_POLICY", "")
        if csp:
            response.headers.setdefault("Content-Security-Policy", csp)
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()",
        )
        return response
