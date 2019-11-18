from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta

from artifacts.models import Artifact, Category
from auctions.models import Auction, Bid
from checkout.forms import OrderForm, MakePaymentForm

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """set the user option to remain anonymous"""
        user.profile.remain_anonymous = True
        user.save()
        
        """create 11 artifacts owned by user"""
        category = Category(name="test", description="test")
        category.save()
        number_of_artifacts = 11
        for artifact_id in range(number_of_artifacts):
            artifact = Artifact.objects.create(
                name = f'Name { artifact_id+1 }',
                description = f'Description { artifact_id+1 }',
                type = 'DATA',
                category = category,
                buy_now_price = 10,
                owner = user,
                sold = True
            )

        artifact_won_by_user = Artifact.objects.create(
            name = f'Name { 12 }',
            description = f'Description { 12 }',
            type = 'DATA',
            category = category
        )     
        
        """
        create an auction with 5 bids
        """

        auction = Auction.objects.create(
            artifact = get_object_or_404(Artifact, pk=12),
            name = f'Auction Name {1}',
            start_date = timezone.now() - timedelta(2),
            end_date = timezone.now() + timedelta(1),
        )

    """
    check failure on no user logged in
    """
    def test_no_user_logged_in(self):
        response = self.client.get('/collection/')
        self.assertFalse(response.status_code==200)
        
    """
    check success on user logged in
    """
    def test_user_logged_in(self):
        testuser = self.client.login(username='TestName', password='test')
        response = self.client.get("/collection/")
        self.assertTrue(response.status_code==200)
    
    """
    check artifacts_won is returned if artifacts have been won
    """
    def test_artifacts_won_list(self):
        testuser = self.client.login(username='TestName', password='test')


        """ create bids """
        number_of_bids = 5
        for bid_id in range(number_of_bids):
            Bid.objects.create(
                bid_amount = bid_id+1,
                bidder = get_object_or_404(User, pk=1),
                auction = get_object_or_404(Auction, pk=1),
                time = timezone.now()
            )  
                        
        """end the auction"""
        auction = get_object_or_404(Auction, pk=1)
        auction.end_date = timezone.now()-timedelta(1)
        auction.save()
        
        response = self.client.get(reverse('view_collection'))
        self.assertTrue(len(response.context['artifacts_won'])==1)
        self.assertEqual(response.context['artifacts_won'][12]['artifact'].name,"Name 12")
        self.assertEqual(response.context['artifacts_won'][12]['bid'],5.00)

    """
    check artifacts_won is not returned if no artifacts have been won
    """
    def test_artifacts_not_won_list(self):
        testuser = self.client.login(username='TestName', password='test')
        """end the auction"""
        auction = get_object_or_404(Auction, pk=1)
        auction.end_date = timezone.now()-timedelta(1)
        auction.save()

        response = self.client.get(reverse('view_collection'))
        self.assertTrue(len(response.context['artifacts_won'])==0)


    """
    check results for owned artifacts are limited to 10 per page
    """
    def test_pagination_is_ten(self):
        testuser = self.client.login(username='TestName', password='test')
        response = self.client.get(reverse('view_collection'))
        self.assertTrue(len(response.context['artifacts_owned']) == 10)
        
    """
    check all results are listed by getting second page and checking the
    results are limited to 1
    """
    def test_all_artifacts_are_listed_in_pagination(self):
        testuser = self.client.login(username='TestName', password='test')

        response = self.client.get("/collection/"+'?page=2')
        self.assertTrue(len(response.context['artifacts_owned']) == 1)   
     

        
