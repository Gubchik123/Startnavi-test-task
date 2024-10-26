from django.test import TestCase
from django.db.models import CASCADE
from django.contrib.auth.models import User

from post.models import Post
from comment.models import Comment
from core.test_mixins import TimeStampedModelTestMixin


class CommentModelTestCase(TimeStampedModelTestMixin, TestCase):
    """Test cases for the Comment model."""

    model = Comment

    def test_content_text_field(self):
        """Test that the content field is a TextField."""
        self._test_field_class_name("content", "TextField")

    def test_is_blocked_boolean_field(self):
        """Test that the is_blocked field is a BooleanField."""
        self._test_field_class_name("is_blocked", "BooleanField")

    def test_is_blocked_default_value(self):
        """Test that the is_blocked field has a default value of False."""
        self.assertFalse(self.model._meta.get_field("is_blocked").default)

    def test_parent_foreign_key(self):
        """Test that the parent field is a ForeignKey."""
        self._test_field_class_name("parent", "ForeignKey")

    def test_parent_self_reference(self):
        """Test that the parent field references the Comment model itself."""
        self.assertEqual(
            self.model._meta.get_field("parent").related_model.__name__,
            "Comment",
        )

    def test_parent_null(self):
        """Test that the parent field allows null values."""
        self.assertTrue(self.model._meta.get_field("parent").null)

    def test_parent_blank(self):
        """Test that the parent field allows blank values."""
        self.assertTrue(self.model._meta.get_field("parent").blank)

    def test_parent_on_delete(self):
        """Test that the parent field has the CASCADE on_delete option."""
        self.assertEqual(
            self.model._meta.get_field("parent").remote_field.on_delete,
            CASCADE,
        )

    def test_parent_related_name(self):
        """Test that the parent field has the related name 'replies'."""
        self.assertEqual(
            self.model._meta.get_field("parent").related_query_name(),
            "replies",
        )

    def test_post_foreign_key(self):
        """Test that the post field is a ForeignKey."""
        self._test_field_class_name("post", "ForeignKey")

    def test_post_related_name(self):
        """Test that the post field has the related name 'comments'."""
        self.assertEqual(
            self.model._meta.get_field("post").related_query_name(),
            "comments",
        )

    def test_post_on_delete(self):
        """Test that the post field has the CASCADE on_delete option."""
        self.assertEqual(
            self.model._meta.get_field("post").remote_field.on_delete,
            CASCADE,
        )

    def test_author_foreign_key(self):
        """Test that the author field is a ForeignKey."""
        self._test_field_class_name("author", "ForeignKey")

    def test_author_related_name(self):
        """Test that the author field has the related name 'comments'."""
        self.assertEqual(
            self.model._meta.get_field("author").related_query_name(),
            "comments",
        )

    def test_author_on_delete(self):
        """Test that the author field has the CASCADE on_delete option."""
        self.assertEqual(
            self.model._meta.get_field("author").remote_field.on_delete,
            CASCADE,
        )

    def test_string_representation(self):
        """Test that the string representation is the author and post."""
        author = User.objects.get_or_create(username="testuser")[0]
        comment = self.model.objects.create(
            content="Test comment",
            post=Post.objects.create(
                title="Test post", content="Test content", author=author
            ),
            author=author,
        )
        self.assertEqual(
            str(comment),
            f"{comment.author} - {comment.post}",
        )

    def test_ordering(self):
        """Test that the default ordering is by created_at and updated_at descending."""
        self.assertEqual(
            self.model._meta.ordering,
            ["-created_at", "-updated_at"],
        )
