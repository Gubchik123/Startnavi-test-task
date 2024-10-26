from django.db.models import Model
from django.contrib.auth.models import User


class ModelTestMixin:
    """Test mixin for models."""

    model: Model

    def _test_field_class_name(self, field_name: str, class_name: str):
        """Test that the the field is of the given class name."""
        self.assertEqual(
            self.model._meta.get_field(field_name).__class__.__name__,
            class_name,
        )


class TimeStampedModelTestMixin(ModelTestMixin):
    """Test mixin for models with TimeStampedModel."""

    def test_created_at_datetime_field(self):
        """Test that the created_at field is a DateTimeField."""
        self._test_field_class_name("created_at", "DateTimeField")

    def test_created_at_auto_now_add(self):
        """Test that the created_at field is auto_now_add."""
        self.assertTrue(self.model._meta.get_field("created_at").auto_now_add)

    def test_updated_at_datetime_field(self):
        """Test that the updated_at field is a DateTimeField."""
        self._test_field_class_name("updated_at", "DateTimeField")

    def test_updated_at_auto_now(self):
        """Test that the updated_at field is auto_now."""
        self.assertTrue(self.model._meta.get_field("updated_at").auto_now)


class IsAuthorOrReadOnlyPermissionTestMixin:
    """Test mixin for views with the IsAuthorOrReadOnly permission."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data."""
        cls.author = User.objects.create_user(
            username="author", password="password"
        )
        cls.user = User.objects.create_user(
            username="user", password="password"
        )

    def test_anonymous_user_cannot_create(self):
        """Test that an anonymous user cannot create the object."""
        response = self.client.post(self.url, {"content": "Comment content"})
        self.assertEqual(response.status_code, 401)

    def test_create_valid(self):
        """Test the creation of the object with valid data."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self._get_valid_data())
        self.assertEqual(response.status_code, 201)

    def test_create_invalid(self):
        """Test the creation of the object with invalid data."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self._get_invalid_data())
        self.assertEqual(response.status_code, 400)

    def test_author_can_edit(self):
        """Test that the author can edit the object."""
        self.client.force_authenticate(user=self.author)
        response = self.client.patch(
            f"{self.url}{self.obj.id}/", {"content": "new text"}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_edit(self):
        """Test that a user cannot edit the object."""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"{self.url}{self.obj.id}/", {"content": "new text"}
        )
        self.assertEqual(response.status_code, 403)

    def test_author_can_delete(self):
        """Test that the author can delete the object."""
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(f"{self.url}{self.obj.id}/")
        self.assertEqual(response.status_code, 204)

    def test_user_cannot_delete(self):
        """Test that a user cannot delete the object."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"{self.url}{self.obj.id}/")
        self.assertEqual(response.status_code, 403)

    def _get_valid_data(self) -> dict:
        """Returns valid data for the object creation."""
        raise NotImplementedError

    def _get_invalid_data(self) -> dict:
        """Returns invalid data for the object creation."""
        raise NotImplementedError
