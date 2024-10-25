from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Comment
from .services import get_ai_response


logger = get_task_logger(__name__)


@shared_task
def generate_comment_answer(comment_id):
    """Task to generate answer on the comment with the given id."""
    logger.info(f"{comment_id=} ({type(comment_id)})")
    comment = Comment.objects.get(pk=comment_id)
    logger.info(f"Auto answering comment {comment.pk}")
    post = comment.post
    ai_comment_answer = get_ai_response(
        prompt=(
            f"You are the author of the post '{post.title}' "
            f"with the following content:\n{post.content}\n\n"
            f"The comment you received from {comment.author.username} is:\n"
            f"{comment.content}\n\n"
            "Please provide a response to the comment as a reply."
        )
    )
    Comment.objects.create(
        content=ai_comment_answer,
        post=post,
        author=post.author,
        parent=comment,
    )
    logger.info(f"Auto answered comment {comment.pk}")
