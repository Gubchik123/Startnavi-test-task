from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""

    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        """Meta options for the PostSerializer class."""

        model = Post
        fields = "__all__"
        extra_kwargs = {
            "auto_comment_answer": {"write_only": True},
            "comment_answer_delay_mins": {"write_only": True},
        }
