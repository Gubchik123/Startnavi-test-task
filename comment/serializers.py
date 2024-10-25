from rest_framework import serializers
from django.core.exceptions import ValidationError

from core.validators import validate_content_

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    def create(self, validated_data):
        """Put the author of the comment as the current user."""
        self._validate_and_block_content(validated_data)
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update the content of the comment."""
        self._validate_and_block_content(validated_data)
        return super().update(instance, validated_data)

    def _validate_and_block_content(self, validated_data):
        """Validate content and block if validation fails."""
        try:
            validate_content_(validated_data["content"])
        except ValidationError:
            validated_data["is_blocked"] = True

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
