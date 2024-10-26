from django.db.models import Model


class ModelTestMixin:
    """Test mixin for models."""

    model: Model

    def _test_field_class_name(self, field_name, class_name):
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
