from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from contextlib import contextmanager
from artifacts.models import Category, Artifact
from .models import Historical_Figure, Event

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

class SetUpData(object):
    @classmethod
    def setUpTestData(cls):
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """set the user option to remain anonymous"""
        user.profile.remain_anonymous = True
        user.save()

        """create artifacts"""
        number_of_categories = 3
        for category_id in range(number_of_categories):
            Category.objects.create(
                name = f'test { category_id+1 }',
                description = f'test description { category_id+1 }'
            )

        Artifact.objects.create(
            name = f'Name { 1 }',
            description = f'Description { 1 }',
            type = "MEDIA",
            category = get_object_or_404(Category, pk=1),
            buy_now_price = 1.00
        )    
    

class TestHistoricalFigureModel(SetUpData, TestCase):
    

    """check error raised if no artifact associated with Figure """
    def test_error_raised_if_no_artifact(self):
        instance = Historical_Figure(
            name = "Test Figure",
            description = "Test description",
            artifact_possessed = None
            )
        self.assertRaises(ValidationError, instance.clean)
    
    """check url description is correct """
    def test_url_description_is_correct(self):

        instance = Historical_Figure(
            name = "Test Figure",
            description = "Test Name 1 description",
            artifact_possessed = get_object_or_404(Artifact, pk=1)
        )
        instance.clean()
        instance.save()
        self.assertEqual(instance.url_description, "Test <a href='/artifacts/artifact/1'>Name 1</a> description")


class TestEventModel(SetUpData, TestCase):
    
    """Test validation error raised if no artifact associated with event"""
    def test_event_artifact_validation(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = None,
        )
        self.assertRaises(ValidationError, instance.clean)
    
    
    """Test day of month validation"""
    def test_day_of_the_month_validation(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = get_object_or_404(Artifact, pk=1),
            month = 2,
            day = 31
        )
        self.assertRaises(ValidationError, instance.clean)
        
    """Second test day of month validation"""
    def test_day_of_the_month_validation_two(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = get_object_or_404(Artifact, pk=1),
            month = 6,
            day = 31
        )
        self.assertRaises(ValidationError, instance.clean)

    """Test day but month missing  validation"""
    def test_day_but_month_missing_validation_two(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = get_object_or_404(Artifact, pk=1),
            day = 31
        )
        self.assertRaises(ValidationError, instance.clean)

    """Test sort year properly assigned for BC"""
    def test_sort_year_assigned_bc(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = get_object_or_404(Artifact, pk=1),
            year = 25,
            bc = "BC",
        )
        instance.clean()
        instance.save()
        self.assertEqual(instance.sort_year, -25)
        
    """Test sort year properly assigned for AD"""
    def test_sort_year_assigned_ad(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = get_object_or_404(Artifact, pk=1),
            year = 25,
            bc = "AD",
        )
        instance.clean()
        instance.save()
        self.assertEqual(instance.sort_year, 25)
    
    """Test month changed from digit to text"""
    def test_change_month(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = get_object_or_404(Artifact, pk=1),
            month = 12
        )
        instance.clean()
        self.assertEqual(instance.month, "December")    

        
    """Test date text properly processed"""
    def test_assign_date(self):
        instance = Event(
            name = "Event 1",
            description = "Test Event",
            artifact = get_object_or_404(Artifact, pk=1),
            day = 23,
            month = 2,
            year = 25,
            bc = "BC",
        )
        instance.clean()
        self.assertEqual(instance.date, "23 February 25 BC")
        
    """check url description is correct """
    def test_url_event_description_is_correct(self):

        instance = Event(
            name = "Test Event",
            description = "Test Event Name 1 description",
            artifact = get_object_or_404(Artifact, pk=1)
        )
        instance.clean()
        self.assertEqual(instance.url_description, "Test Event <a href='/artifacts/artifact/1'>Name 1</a> description")

    """check url description is correct """
    def test_url_event_description_with_historical_figure_is_correct(self):

        Historical_Figure.objects.create(
            name = "Test Figure",
            description = "Test Name 1 description",
            artifact_possessed = get_object_or_404(Artifact, pk=1)
        )
        instance = Event(
            name = "Test Event",
            description = "Test Event Test Figure used Name 1 description",
            artifact = get_object_or_404(Artifact, pk=1),
            historical_figure = get_object_or_404(Historical_Figure, pk=1)
        )
        instance.clean()
        self.assertEqual(instance.url_description, "Test Event <a href='/history/historical_figure/1'>Test Figure</a> used <a href='/artifacts/artifact/1'>Name 1</a> description")
