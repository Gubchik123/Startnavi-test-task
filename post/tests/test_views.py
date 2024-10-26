from django.utils import timezone
from rest_framework.test import APITestCase

from post.models import Post
from comment.models import Comment
from core.test_mixins import IsAuthorOrReadOnlyPermissionTestMixin


class PostViewSetAPITestCase(
    IsAuthorOrReadOnlyPermissionTestMixin, APITestCase
):
    """Test cases for the PostViewSet."""

    url = "/api/v1/posts/"

    @classmethod
    def setUpTestData(cls):
        """Creates test data."""
        super().setUpTestData()
        cls.obj = Post.objects.create(
            title="Post title", content="Post content", author=cls.author
        )
        for count in range(10):
            Post.objects.create(
                title=f"Post title {count}",
                content=f"Post content {count}",
                author=cls.author,
            )

    def test_list_posts(self):
        """Tests the list endpoint."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 11)

    def test_get_post(self):
        """Tests the retrieve endpoint."""
        response = self.client.get(f"{self.url}{self.obj.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.obj.title)

    def test_create_with_censored_word(self):
        """Tests the creation of the post with a censored word."""
        self.client.force_authenticate(user=self.user)
        data = self._get_valid_data()
        data["content"] = "Something bad"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

    def test_comments_analytics_with_invalid_dates(self):
        """Tests the comments_analytics action with invalid dates."""
        response = self.client.get(
            f"{self.url}{self.obj.id}/comments_analytics/",
            {"date_from": "string", "date_to": "string"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid date range")

    def test_comments_analytics(self):
        """Tests the comments_analytics action."""
        for _ in range(10):
            Comment.objects.create(
                post=self.obj, content="Comment content", author=self.user
            )
        for _ in range(5):
            Comment.objects.create(
                post=self.obj,
                content="Comment bad",
                author=self.user,
                is_blocked=True,
            )
        today = timezone.now().date()
        response = self.client.get(
            f"{self.url}{self.obj.id}/comments_analytics/",
            {"date_from": today, "date_to": today},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "total_comments": 15,
                    "blocked_comments": 5,
                    "created_at__date": today.strftime("%Y-%m-%d"),
                }
            ],
        )

    def _get_valid_data(self) -> dict:
        """Returns valid data for the post creation."""
        return {
            "title": "Post title",
            "content": "Post content",
            "author": self.user.id,
        }

    def _get_invalid_data(self) -> dict:
        """Returns invalid data for the post creation."""
        return {"content": ""}
