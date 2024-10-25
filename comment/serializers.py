from rest_framework.serializers import ModelSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    """Serializer for the Comment model."""

    def create(self, validated_data):
        """Put the author of the comment as the current user."""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        """Meta options for the CommentSerializer class."""

        model = Comment
        exclude = ["is_blocked", "author"]
