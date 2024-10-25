from rest_framework import serializers

from comment.serializers import PostCommentSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""

    author = serializers.CharField(source="author.username", read_only=True)

    def get_fields(self) -> dict[str, serializers.Field]:
        """Returns fields with nested serializers for the retrieve action."""
        fields = super().get_fields()
        view = self.context.get("view")
        if view and view.action == "retrieve":
            fields["comments"] = PostCommentSerializer(many=True)
        return fields

    def create(self, validated_data):
        """Put the author of the post as the current user."""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        """Meta options for the PostSerializer class."""

        model = Post
        fields = "__all__"
        extra_kwargs = {
            "auto_comment_answer": {"write_only": True},
            "comment_answer_delay_mins": {"write_only": True},
        }
