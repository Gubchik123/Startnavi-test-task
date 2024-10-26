from rest_framework.test import APITestCase

from post.models import Post
from comment.models import Comment
from core.test_mixins import IsAuthorOrReadOnlyPermissionTestMixin


class CommentViewSetAPITestCase(
    IsAuthorOrReadOnlyPermissionTestMixin, APITestCase
):
    """Test cases for the CommentViewSet."""

    url = "/api/v1/comments/"

    @classmethod
    def setUpTestData(cls):
        """Creates test data."""
        super().setUpTestData()
        post = Post.objects.create(
            title="Post title", content="Post content", author=cls.author
        )
        cls.obj = Comment.objects.create(
            content="Comment content", post=post, author=cls.author
        )

    def test_list_comments(self):
        """Tests that the list endpoint is disabled."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_get_comment(self):
        """Tests that the detail endpoint is disabled."""
        response = self.client.get(f"{self.url}{self.obj.id}/")
        self.assertEqual(response.status_code, 405)

    def test_create_with_censored_word(self):
        """Tests the creation of the comment with a censored word."""
        self.client.force_authenticate(user=self.user)
        data = self._get_valid_data()
        data["content"] = "Something bad"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Comment.objects.get(content="Something bad").is_blocked
        )

    def _get_valid_data(self) -> dict:
        """Returns valid data for the comment creation."""
        post = Post.objects.create(
            title="Post title", content="Post content", author=self.user
        )
        return {
            "content": "Comment content",
            "post": post.id,
            "author": self.user.id,
        }

    def _get_invalid_data(self) -> dict:
        """Returns invalid data for the comment creation."""
        return {"content": ""}
