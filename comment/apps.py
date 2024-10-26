from django.apps import AppConfig


class CommentConfig(AppConfig):
    """App config for the 'comment' app."""

    name = "comment"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """Imports signals when the app is ready."""
        import comment.signals
