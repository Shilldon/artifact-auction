from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta

from .models import Review
from .forms import ReviewForm

from artifacts.models import Artifact, Category


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """set the user option to remain anonymous"""
        user.profile.remain_anonymous = True
        user.save()

        """create artifacts"""
        category = Category(name="test", description="test")
        category.save()
        artifact = Artifact.objects.create(
            name = f'Name { 1 }',
            description = f'Description { 1 }',
            type = 'DATA',
            category = category,
            sold = True,
            owner = user
        )            


    """
    check model returns correct str
    """
    def test_check_correct_return(self):
        artifact = get_object_or_404(Artifact, pk=1)
        review = Review(
            description="Test",
            rating = 5,
            reviewer = get_object_or_404(User, pk=1),
            artifact = artifact
        )
        self.assertEquals(str(review), artifact.name)