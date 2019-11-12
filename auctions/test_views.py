from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import Auction
from .views import get_bidder
from artifacts.models import Artifact, Category
from bids.models import Bid

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """set the user option to remain anonymous"""
        user.profile.remain_anonymous = True
        user.save()
        
        """create 2 artifacts"""
        category = Category(name="test", description="test")
        category.save()
        number_of_artifacts = 2
        for artifact_id in range(number_of_artifacts):
            Artifact.objects.create(
                name = f'Name { artifact_id+1 }',
                description = f'Description { artifact_id+1 }',
                type = 'DATA',
                category = category
            )
        
        """create an auction"""
        auction = Auction.objects.create(
            artifact = get_object_or_404(Artifact, pk=1),
            name = f'Auction Name {1}',
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1)            
        )

        """create 5 bids for the auction"""
        number_of_bids = 5
        for bid_id in range(number_of_bids):
            Bid.objects.create(
                bid_amount = bid_id+1,
                bidder = user,
                auction = auction,
                time = timezone.now()
            )  

        """create second auction with no bids"""
        Auction.objects.create(
            artifact = get_object_or_404(Artifact, pk=2),
            name = f'Auction Name {2}',
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1)            
        )
            

    """check that the bidder name is returned as anonymous if another user
    views the page"""
    def test_get_bidder_details_to_return_anonymous_if_user_is_anonymous(self):
        """set up logged in user"""
        page = self.client.get("/artifacts/artifact/1")
        page.user = User.objects.create_user(username='TestName1', email='test1@…', password='test')
        self.assertEqual(get_bidder(page, 1), "Anonymous")    
        
    """check that the bidder name is returned as None if there are no bids"""
    def test_get_bidder_details_return_none_if_no_bids(self):
        """set up logged in user"""
        page = self.client.get("/artifacts/artifact/2")
        page.user = User.objects.create_user(username='TestName1', email='test1@…', password='test')
        self.assertIsNone(get_bidder(page, 2))    

