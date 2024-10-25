from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Permission class to check if the user is the author of the object."""

    def has_object_permission(self, request, view, obj):
        """Check if the user is the author of the object."""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
