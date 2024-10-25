from django.db import models
from django.contrib.auth.models import User

from post.models import Post


class Comment(models.Model):
    """Model representing a comment on a post."""

    content = models.TextField()
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        """Returns the author and post as the string representation of the Comment model"""
        return f"{self.user} - {self.post}"

    class Meta:
        """Meta options for the Comment model."""

        ordering = ["-created_at", "-updated_at"]
