from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    def create(self, validated_data):
        """Put the author of the comment as the current user."""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        """Meta options for the CommentSerializer class."""

        model = Comment
        exclude = ["is_blocked", "author"]


class _RecursiveSerializer(serializers.Serializer):
    """Serializer for recursive displaying."""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class _FilterCommentSerializer(serializers.ListSerializer):
    """Serializer for filtering comments."""

    def to_representation(self, data):
        data = data.filter(parent=None, is_blocked=False)
        return super().to_representation(data)


class PostCommentSerializer(serializers.ModelSerializer):
    """Serializer for post comments."""

    replies = _RecursiveSerializer(many=True)
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        """Meta options for the PostCommentSerializer."""

        model = Comment
        exclude = ("is_blocked", "post", "parent")
        list_serializer_class = _FilterCommentSerializer
