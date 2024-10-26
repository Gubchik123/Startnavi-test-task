from django.db.models import Model
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Permission class to check if the user is the author of the object."""

    def has_object_permission(
        self, request: Request, view, obj: Model
    ) -> bool:
        """Check if the user is the author of the object."""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
