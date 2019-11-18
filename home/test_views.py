from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta

from artifacts.models import Artifact, Category
from auctions.models import Auction, Bid

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
        number_of_artifacts = 4
        for artifact_id in range(number_of_artifacts):
            artifact = Artifact.objects.create(
                name = f'Name { artifact_id+1 }',
                description = f'Description { artifact_id+1 }',
                type = 'DATA',
                category = category
            )            
            """create an auction for each artifact"""
            auction = Auction.objects.create(
                artifact = artifact,
                name = f'Auction Name { artifact_id+1 }',
                start_date = timezone.now() - timedelta(3) ,
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
    """
    Check page renders
    """
    def test_display_historical_figure_render(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    """
    check context for more than 1 live auction
    """
    
    def test_context_results_more_than_1_auction(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['auctions']), 4)
        self.assertEqual(response.context['auction_status'], "Current auctions")
    
    """
    check context for no live auctions
    """
    
    def test_context_results_no_auction(self):
        
        auctions = Auction.objects.all()
        for auction in auctions:
            auction.end_date = timezone.now() - timedelta(1)
            auction.save()
            
        response = self.client.get('/')
        self.assertEqual(len(response.context['auctions']), 0)
        self.assertEqual(response.context['auction_status'], "No live auctions")

    """
    check context for one live auction
    """
    
    def test_context_results_one_auction(self):
        
        auctions = Auction.objects.all()
        for auction in auctions:
            auction.end_date = timezone.now() - timedelta(1)
            auction.save()
        
        auction = get_object_or_404(Auction, pk=1)
        auction.end_date = timezone.now() + timedelta(1)
        auction.save()
            
        response = self.client.get('/')
        self.assertEqual(len(response.context['auctions']), 1)
        self.assertEqual(response.context['auction_status'], "Current auction")
