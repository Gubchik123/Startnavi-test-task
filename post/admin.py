from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin class for the Post model."""

    search_fields = ("title", "content")
    search_help_text = "Search by title or content"
    list_display = (
        "title",
        "author",
        "auto_comment_answer",
        "created_at",
        "updated_at",
    )
    list_display_links = ("title",)
    list_filter = ("auto_comment_answer", "created_at", "updated_at")
