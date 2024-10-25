from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAuthorOrReadOnly

from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    """View set for the Post model."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
