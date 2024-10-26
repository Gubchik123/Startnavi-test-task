from django.test import TestCase
from django.db.models import CASCADE
from django.contrib.auth.models import User

from post.models import Post
from core.validators import validate_content_
from core.test_mixins import TimeStampedModelTestMixin


class PostModelTestCase(TimeStampedModelTestMixin, TestCase):
    """Test cases for the Post model."""

    model = Post

    def test_title_char_field(self):
        """Test that the title field is a CharField."""
        self._test_field_class_name("title", "CharField")

    def test_title_max_length(self):
        """Test that the title field has a max length of 255."""
        self.assertEqual(self.model._meta.get_field("title").max_length, 255)

    def test_content_text_field(self):
        """Test that the content field is a TextField."""
        self._test_field_class_name("content", "TextField")

    def test_content_validators(self):
        """Test that the content field has the content validator."""
        self.assertIn(
            validate_content_, self.model._meta.get_field("content").validators
        )

    def test_auto_comment_answer_boolean_field(self):
        """Test that the auto_comment_answer field is a BooleanField."""
        self._test_field_class_name("auto_comment_answer", "BooleanField")

    def test_auto_comment_answer_default_value(self):
        """Test that the auto_comment_answer field has a default value of False."""
        self.assertFalse(
            self.model._meta.get_field("auto_comment_answer").default
        )

    def test_comment_answer_delay_mins_positive_integer_field(self):
        """Test that the comment_answer_delay_mins field is a PositiveIntegerField."""
        self._test_field_class_name(
            "comment_answer_delay_mins", "PositiveIntegerField"
        )

    def test_comment_answer_delay_mins_default_value(self):
        """Test that the comment_answer_delay_mins field has a default value of 0."""
        self.assertEqual(
            self.model._meta.get_field("comment_answer_delay_mins").default, 0
        )

    def test_author_foreign_key(self):
        """Test that the author field is a ForeignKey."""
        self._test_field_class_name("author", "ForeignKey")

    def test_author_on_delete(self):
        """Test that the author field has the CASCADE on_delete option."""
        self.assertEqual(
            self.model._meta.get_field("author").remote_field.on_delete,
            CASCADE,
        )

    def test_author_related_name(self):
        """Test that the author field has the related name 'posts'."""
        self.assertEqual(
            self.model._meta.get_field("author").related_query_name(),
            "posts",
        )

    def test_string_representation(self):
        """Test that the string representation is the title."""
        post = self.model(
            title="My Post",
            content="My Content",
            author=User.objects.get_or_create(username="testuser")[0],
        )
        self.assertEqual(str(post), "My Post")

    def test_ordering(self):
        """Test that the default ordering is by created_at, updated_at, and title."""
        self.assertEqual(
            self.model._meta.ordering,
            ["-created_at", "-updated_at", "title"],
        )
