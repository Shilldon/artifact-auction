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
    Check page renders
    """
    def test_add_review_display(self):
        response = self.client.get('/review/add_review/1')
        self.assertEqual(response.status_code, 200)
    
    """
    Check form passed in context
    """
    def test_form_rendered(self):
        testuser = self.client.login(username='TestName', password='test')
        response = self.client.get("/review/add_review/1")
        self.assertIsInstance(response.context['review_form'], ReviewForm)


    """
    Check completed review form in context
    """
    def test_completed_form_rendered(self):
        testuser = self.client.login(username='TestName', password='test')
        """
        create review
        """
        review = Review.objects.create(
            description="test description",
            rating = 5,
            reviewer = get_object_or_404(User, pk=1),
            artifact = get_object_or_404(Artifact, pk=1)
            )
        response = self.client.get("/review/add_review/1")
        self.assertEqual(response.context['review_form'].initial['description'], "test description")

    """
    Check review can be added
    """
    def test_valid_review(self):
        testuser = self.client.login(username='TestName', password='test')
        
        response = self.client.post("/review/add_review/1", { 'description' : 'test', 'rating' : 5})
        self.assertRedirects(response, expected_url=reverse('display_artifact', kwargs={ 'id' : 1 }), status_code=302, target_status_code=200)
        self.assertTrue(get_object_or_404(Review,pk=1))
        self.assertTrue(get_object_or_404(Review,pk=1).description=="test")
        self.assertTrue(get_object_or_404(Review,pk=1).rating==5)
        
        
    """
    Check delete_review
    """

    def test_review_is_deleted(self):
        testuser = self.client.login(username='TestName', password='test')
        """
        create a review
        """
        
        review = Review.objects.create(
            description="test description",
            rating = 5,
            reviewer = get_object_or_404(User, pk=1),
            artifact = get_object_or_404(Artifact, pk=1)
            )

        response = self.client.post("/review/delete_review/1", follow=True)
        try:
            review = get_object_or_404(Review,pk=1)
        except:
            review = None
        self.assertIsNone(review)
        self.assertRedirects(response, expected_url=reverse('display_artifact', kwargs={ 'id' : 1 }), status_code=302, target_status_code=200)
        
 
