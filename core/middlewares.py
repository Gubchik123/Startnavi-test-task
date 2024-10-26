import json
from typing import Callable

from django.http import HttpRequest, HttpResponse


class NonHtmlDebugToolbarMiddleware:
    """Middleware to put JSON in HTML for the Django Debug Toolbar."""

    def __init__(self, get_response: Callable):
        """Initializes the middleware with the given get_response."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Puts JSON in HTML if the debug parameter is present."""
        response = self.get_response(request)
        if (
            request.GET.get("debug", None) is not None
            and response["Content-Type"] == "application/json"
        ):
            content = json.dumps(
                json.loads(response.content), sort_keys=True, indent=2
            )
            response = HttpResponse(
                "<html><body><pre>{}</pre></body></html>".format(content)
            )
        return response
