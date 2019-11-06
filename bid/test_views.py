from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta

from .models import Bids
from artifacts.models import Artifact, Category
from auctions.models import Auction

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """set the user option to remain anonymous"""
        user.profile.remain_anonymous = True
        user.save()
        
        """create an artifact"""
        category = Category(name="test", description="test")
        category.save()
        artifact = Artifact.objects.create(
            name = f'Name { 1 }',
            description = f'Description { 1 }',
            type = 'DATA',
            category = category
        )
        
        """create an auction"""
        auction = Auction.objects.create(
            artifact = artifact,
            name = f'Auction Name {1}',
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1)            
        )

        """create 5 bids for the auction"""
        number_of_bids = 5
        for bid_id in range(number_of_bids):
            Bids.objects.create(
                bid_amount = bid_id+1,
                bidder = user,
                auction = auction,
                time = timezone.now()
            )  
            

    """
    Test check bid returns user to same page if bid is lower than current bid
    """
    def test_check_bid_lower_than_current(self):
        c = Client()
        response = c.post('/artifacts/artifact/1', { "amount_bid" : 1 })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "display_artifact.html")        

    """
    Test check bid returns false for invalid form
    """
    def test_check_bid_higher_than_current(self):
        """set up logged in user"""
        c = Client()
        page = c.post('/artifacts/artifact/1', { "amount_bid" : 10 })

        page.user = User.objects.create_user(username='TestName1', email='test1@…', password='test')
        #self.assertIn('_auth_user_id', self.client.session)    
        #self.assertEqual(page.status_code, 200)
        #self.assertTemplateUsed(page, "artifacts.html")   
        
    
    """
    Test check bid returns false for bid lower than current bid
    """
    def test_check_bid_returns_false_on_low_bid(self):
        c = Client()
        response = c.get('/display_artifacts/1/check_bid', { "amount_bid" : 1 })
        #self.assertFalse(response.content)

    """
    Test check bid returns true for bid higher than current bid
    """
    def test_check_bid_returns_true_on_high_bid(self):
        c = Client()
        response = c.get('/display_artifacts/1/check_bid', { "amount_bid" : 10 })
        #self.assertTrue(response.content)