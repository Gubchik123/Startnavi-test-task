from django.db.models import Count, Q

from comment.models import Comment


def get_comments_analytics(post_id, date_from, date_to):
    """Return analytics about comments
    that were added to posts during a certain period."""
    comments = (
        Comment.objects.filter(
            post_id=post_id,
            created_at__date__gte=date_from,
            created_at__date__lte=date_to,
        )
        .values("created_at__date")
        .annotate(
            total_comments=Count("id"),
            blocked_comments=Count("id", filter=Q(is_blocked=True)),
        )
        .order_by("created_at__date")
    )
    return list(comments)
