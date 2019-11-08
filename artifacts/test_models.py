from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from contextlib import contextmanager
from .models import Category, Artifact

class ValidationErrorTestMixin(object):

    @contextmanager
    def assertValidationErrors(self, fields):
        """
        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))


class TestCategoryModel(ValidationErrorTestMixin, TestCase):
    """check the category model correctly defaults to blank fields"""
    def test_category_defaults_to_blank(self):
        category = Category()
        category.save()
        self.assertEqual(category.name, "")
        self.assertEqual(category.description,"")

    """check model raises errors if required fields are blank"""
    def test_category_required_fields(self):
        category = Category()
        with self.assertValidationErrors(['name','description']):
            category.full_clean()

class TestArtifactModel(ValidationErrorTestMixin, TestCase):
    """check model raises errors if required fields are blank"""
    def test_required_fields(self):
        artifact = Artifact()
        with self.assertValidationErrors(['name','category','type','description']):
            artifact.full_clean()

    """check sold status defaults to false"""
    def test_sold_defaults_to_false(self):
        artifact = Artifact()
        self.assertFalse(artifact.sold)

    """
    check model raises error sold is set to true and owner is blank and
    vice versa
    """
    def test_interaction_of_sold_and_owner_fields_no_owner_set_sold_is_true(self):
        category = Category(name="test", description="test")
        artifact = Artifact(name="test", category=category, description="test", type="DATA", sold=True)
        self.assertRaises(ValidationError, artifact.clean)

    def test_interaction_of_sold_and_owner_fields_owner_set_sold_is_false(self):
        category = Category(name="test", description="test")
        owner = User()
        artifact = Artifact(name="test", category=category, description="test", type="DATA", owner=owner, sold=False)
        self.assertRaises(ValidationError, artifact.clean)
        