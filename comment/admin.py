from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin class for the Comment model."""

    search_fields = ["content"]
    search_help_text = "Search by content"
    list_display = [
        "mini_content",
        "post",
        "author",
        "parent",
        "is_blocked",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["mini_content"]
    list_filter = ["is_blocked", "created_at", "updated_at"]

    def mini_content(self, comment: Comment) -> str:
        """Returns the first 50 characters of the given comment content."""
        return comment.content[:50]
