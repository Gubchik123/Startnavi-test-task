from typing import Optional

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from core.permissions import IsAuthorOrReadOnly

from .models import Post
from .serializers import PostSerializer
from .services import get_comments_analytics


class PostViewSet(ModelViewSet):
    """View set for the Post model."""

    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    @action(detail=True, methods=["get"])
    def comments_analytics(
        self, request: Request, pk: Optional[int] = None
    ) -> JsonResponse:
        """Returns analytics about comments
        that were added to posts during a certain period."""
        date_from = parse_date(request.query_params.get("date_from", ""))
        date_to = parse_date(request.query_params.get("date_to", ""))

        if not date_from or not date_to:
            return JsonResponse({"error": "Invalid date range"}, status=400)
        return JsonResponse(
            get_comments_analytics(pk, date_from, date_to), safe=False
        )
