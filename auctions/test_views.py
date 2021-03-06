import json

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta

from .models import Auction, Bid
from .views import get_bidder
from artifacts.models import Artifact, Category

class TestAuctionViews(TestCase):

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

class TestBidViews(TestCase):

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
        
        artifact_not_in_auction = Artifact.objects.create(
            name = f'Name { 2 }',
            description = f'Description { 2 }',
            type = 'DATA',
            category = category
        )     
        
        artifact_sold = Artifact.objects.create(
            name = f'Name { 3 }',
            description = f'Description { 3 }',
            type = 'DATA',
            category = category,
            sold = True
        )        

        artifact_not_bidded_on = Artifact.objects.create(
            name = f'Name { 4 }',
            description = f'Description { 4 }',
            type = 'DATA',
            category = category,
            sold = False
        )        
        
        
        """create an auction"""
        auction = Auction.objects.create(
            artifact = artifact,
            name = f'Auction Name {1}',
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1),
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
        auction = Auction.objects.create(
            artifact = get_object_or_404(Artifact, pk=4),
            name = f'Auction Name {4}',
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1),
        )

            
    """ 
    Test check bid
    """


    """
    Test check bid returns user to same page if bid is lower than current bid
    """
    def test_check_bid_lower_than_current(self):
        c = Client()
        response = c.post('/artifacts/artifact/1', { "amount_bid" : 1 })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "display_artifact.html")        

    """
    Test check bid returns user to artifacts list if bid is higher than current bid
    """
    def test_check_bid_higher_than_current(self):
        """set up logged in user"""
        testuser = self.client.login(username='TestName', password='test')
        page = self.client.post('/artifacts/artifact/1', { "amount_bid" : 10 }, follow=True)
        self.assertRedirects(page, expected_url=reverse('display_artifact', kwargs={ "id" : 1 } ), status_code=302, target_status_code=200)
        
    """
    Check get bid
    """
    """check get bid returns correct for artifact in auction"""
    def test_get_bid_reponse_in_auction(self):
        c = Client()
        response = c.get('/artifacts/list/get_bid', { "artifact_id" : 1 })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['in_auction'], True)
        self.assertEqual(content['current_bid'], 5.0)

    """check get bid returns correct for artifact not in auction"""
    def test_get_bid_reponse_not_in_auction(self):
        c = Client()
        response = c.get('/artifacts/list/get_bid', { "artifact_id" : 2 })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Name 2: Not yet listed for auction.')
        
    """check get bid returns correct for artifact already sold"""
    def test_get_bid_reponse_artifact_sold(self):
        c = Client()
        response = c.get('/artifacts/list/get_bid', { "artifact_id" : 3 })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Name 3 has already sold, no auction information')
        
    """check get_bid 0 for no bid in auction"""
    def test_get_bid_zero_bids_reponse_in_auction(self):
        c = Client()
        response = c.get('/artifacts/list/get_bid', { "artifact_id" :4 })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['in_auction'], True)
        self.assertEqual(content['current_bid'], 0)

    """check check_bid 0 for no bid in auction"""
    def test_check_bid_zero_bids_reponse_in_auction(self):
        testuser = self.client.login(username='TestName', password='test')
        page = self.client.post('/artifacts/artifact/4', { "amount_bid" : 10 }, follow=True)
        self.assertEqual(page.context['current_bid'], 10.0)
        self.assertRedirects(page, expected_url=reverse('display_artifact', kwargs={ "id" : 4 } ), status_code=302, target_status_code=200)
