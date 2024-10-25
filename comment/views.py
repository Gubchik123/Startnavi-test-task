from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsAuthorOrReadOnly

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """Write-only viewset for the Comment model."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
