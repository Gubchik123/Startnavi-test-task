from django.dispatch import receiver
from django.utils.timezone import timedelta
from django.db.models.signals import post_save
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from .models import Comment


@receiver(post_save, sender=Comment)
def handle_new_comment(instance: Comment, created: bool, **kwargs):
    """Handles new comment creation.
    If the comment is not blocked, has no parent, and the post has auto_comment_answer enabled,
    schedules a task to auto answer the comment."""
    if (
        created
        and not instance.is_blocked
        and instance.parent is None
        and instance.post.auto_comment_answer
    ):
        PeriodicTask.objects.create(
            name=f"Auto comment answer for comment {instance.pk}",
            task="comment.tasks.generate_comment_answer",
            clocked=ClockedSchedule.objects.get_or_create(
                clocked_time=instance.created_at
                + timedelta(minutes=instance.post.comment_answer_delay_mins)
            )[0],
            args=f"[{instance.pk}]",
            one_off=True,
        )
