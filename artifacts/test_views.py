from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Category, Artifact
from auctions.models import Auction
from bids.models import Bid
from history.models import Historical_Figure, Event
from reviews.models import Review

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """create 15 artifacts"""
        number_of_artifacts = 15
        category = Category(name="test", description="test")
        category.save()
        for artifact_id in range(number_of_artifacts):
            artifact = Artifact.objects.create(
                name = f'Name { artifact_id }',
                description = f'Description { artifact_id }',
                type = 'DATA',
                category = category
            )
            """ create an event and historical figure for 10 artifacts"""
        number_of_histories = 10
        for artifact_id in range(number_of_histories):
            artifact = get_object_or_404(Artifact, pk=artifact_id+1)
            Historical_Figure.objects.create(
                artifact_possessed = artifact,
                name = f'Figure name { artifact_id }',
                description = f'Figure description { artifact_id }'
            )
            Event.objects.create(
                artifact = artifact,
                name = f'Event name { artifact_id }',
                description = f'Event description { artifact_id }'
            )                
        
        """create 6 auctions for 6 artifacts with incrementing number of bids 
        between 1 and 5 and bid amounts from 1.00 to 5.00 and one auction
        with no bids"""
        
        number_of_auctions = 5
        bidder = user 
        for auction_id in range(number_of_auctions):
            artifact = get_object_or_404(Artifact, pk=auction_id+1)
            auction = Auction.objects.create(
                artifact = artifact,
                name = f'Name { auction_id }',
                start_date = timezone.now(),
                end_date = timezone.now() + timedelta(1)
                )
            number_of_bids = auction_id+1
            for bid_id in range(number_of_bids):
                Bid.objects.create(
                    bid_amount = bid_id+1,
                    bidder = bidder,
                    auction = auction,
                    time = timezone.now()
                )
        artifact = get_object_or_404(Artifact, pk=6)
        auction = Auction.objects.create(
            artifact = artifact,
            name = f'Name { auction_id }',
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1)
            )
            
        
        """create a review of artifact 1"""
        artifact = get_object_or_404(Artifact, pk=1)
        artifact.sold = True
        artifact.owner = user
        artifact.save()
        Review.objects.create(
            description = "Review",
            rating = 5,
            artifact = artifact,
            reviewer = user
        )

    """
    check display of single artifact
    
    """
    """check template used and page displays"""
    def test_get_single_artifact(self):
        page = self.client.get("/artifacts/artifact/1")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "display_artifact.html")
    
    def test_get_invalid_artifact_should_fail(self):
        page = self.client.get("/artifacts/artifact/16")
        self.assertEqual(page.status_code, 404)

    """check the auction and bid details are passed in context"""
    def test_auction_passed(self):
        page = self.client.get("/artifacts/artifact/2")
        auction=get_object_or_404(Auction, pk=2)
        self.assertTrue(page.context['auction']==auction)
        self.assertTrue(len(page.context['bids'])==2)
        self.assertQuerysetEqual(page.context['bids'], ["<Bid: Name 1: 1.00>", "<Bid: Name 1: 2.00>"], ordered=False)
        self.assertEqual(page.context['bidder_name'].username, 'TestName')
        self.assertEqual(page.context['current_bidder'].username, 'TestName')
        self.assertEqual(page.context['current_bid'], 2.00)
        
    """check bid details are set to null if no bids associated
    with the artifact"""
    def test_null_bid_information(self):
        page = self.client.get("/artifacts/artifact/10")  
        self.assertEqual(page.context['bidder_name'], "")
        self.assertEqual(page.context['current_bid'], 0)
        self.assertIsNone(page.context['current_bidder'])
        
       
    """check history details passed in context"""
    def test_history_passed(self):
        page = self.client.get("/artifacts/artifact/1")
        self.assertEqual(page.context['events'][0].name, "Event name 0")
        self.assertEqual(page.context['historical_figures'][0].name, "Figure name 0")

    """check for no events in artifact history"""
    def test_no_events_passed(self):
        page = self.client.get("/artifacts/artifact/15")
        self.assertEqual(len(page.context['events']), 0)

    """check no bidder information is passed if there are no bids in the 
    artifact auction"""
    def test_no_bids_in_artifact_auction(self):
        page = self.client.get("/artifacts/artifact/6")
        self.assertIsNone(page.context['current_bidder'])    

    """check review passed in context"""
    def test_review_passed(self):
        page = self.client.get("/artifacts/artifact/1")
        self.assertEqual(page.context['review'].description, 'Review')
        self.assertEqual(page.context['review'].rating, 5)
        self.assertEqual(page.context['review'].reviewer.username, 'TestName')



    
    """check display of list of artifacts"""
    """check the correct template is displayed"""
    def test_view_url_exists_at_desired_location(self):
        page = self.client.get("/artifacts/list/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "artifacts.html")  
    
    """check results are limited to 10 per page"""
    def test_pagination_is_ten(self):
        page = self.client.get(reverse('artifacts_list'))
        self.assertEqual(page.status_code, 200)
        self.assertTrue(len(page.context['artifacts_list']) == 10)
        
    """check all results are listed by getting second page and checking the
    results are limited to 5"""
    def test_all_artifacts_are_listed(self):
        page = self.client.get(reverse('artifacts_list')+'?page=2')
        self.assertEqual(page.status_code, 200)
        self.assertTrue(len(page.context['artifacts_list']) == 5)
        
    """check all auctions are returned as context"""
    def test_all_auctions_are_in_context(self):
        page = self.client.get(reverse('artifacts_list'))
        self.assertTrue(len(page.context['auctions']) == 6)
    
    """check only highest bids are returned as context"""
    def test_only_highest_bids_are_in_context(self):
        page = self.client.get(reverse('artifacts_list'))
        self.assertTrue(len(page.context['auction_bids']) == 6)
        self.assertTrue(list(page.context['auction_bids'].values()) == ['1.00','2.00','3.00','4.00','5.00', 0])
    
    """check return empty bids list if no bids in auction"""
    def test_no_bids_in_auction(self):
        page = self.client.get(reverse('artifacts_list'))
        artifact = get_object_or_404(Artifact, pk=6)
        self.assertTrue(page.context['auction_bids'][artifact] == 0)
    
    """check live auctions returned if there are any"""
    def test_live_auctions_returned(self):
        page = self.client.get(reverse('artifacts_list', kwargs={"index_search" : 1}))
        self.assertEquals(len(page.context['auctions']), 6)
    
    