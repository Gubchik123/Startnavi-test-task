from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedModel
from core.validators import validate_content_


class Post(TimeStampedModel):
    """Model representing a post."""

    title = models.CharField(max_length=255)
    content = models.TextField(validators=[validate_content_])
    auto_comment_answer = models.BooleanField(default=False)
    comment_answer_delay_mins = models.IntegerField(default=0)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self):
        """Returns the title as the string representation of the Post model."""
        return self.title

    class Meta:
        """Meta options for the Post model."""

        ordering = ["-created_at", "-updated_at", "title"]
