from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta

from bids.models import Bid
from artifacts.models import Artifact, Category
from auctions.models import Auction
from checkout.forms import OrderForm, MakePaymentForm

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
            category = category,
            buy_now_price = 10
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
        
        """create an auction"""
        auction = Auction.objects.create(
            artifact = artifact,
            name = f'Auction Name {1}',
            start_date = timezone.now() - timedelta(2),
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
            
    """
    test checkout
    """
    """
    check failure on no user logged in
    """
    def test_no_user_logged_in(self):
        response = self.client.get("/checkout/")
        self.assertFalse(response.status_code == 200)
        
    """
    check success on user logged in
    """
    def test_user_logged_in(self):
        testuser = self.client.login(username='TestName', password='test')
        response = self.client.get("/checkout/")
        self.assertTrue(response.status_code == 200)

    """
    check forms rendered
    """
    def test_forms_rendered(self):
        testuser = self.client.login(username='TestName', password='test')
        response = self.client.get("/checkout/")
        self.assertIsInstance(response.context['order_form'], OrderForm)
        self.assertIsInstance(response.context['payment_form'], MakePaymentForm)
    
    """
    check error on submitting invalid payment form
    """
    def test_message_on_invalid_form(self):
        testuser = self.client.login(username='TestName', password='test')
        response = self.client.post("/checkout/", {})
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Unable to take payment. Please try again.')
    
    
    """
    check error on trying to pay for artifact that has already sold
    """
    def test_message_on_artifact_already_sold(self):
        testuser = self.client.login(username='TestName', password='test')
        """ 
        set up a session collection with 2 artifacts
        """
        session = self.client.session
        collection = {}
        collection[3] = collection.get(3, {'price' : 10, 'buy_now' : 0 })
        collection[1] = collection.get(1,{'price' : 20, 'buy_now' : 0 })
        session['collection'] = collection
        session.save() 

        response = self.client.post("/checkout/", {
            'full_name' : 'test', 
            'phone_number' : 'test', 
            'street_address1' : 'test', 
            'street_address2' : 'test', 
            'town_or_city' : 'test', 
            'county' : 'test',
            'postcode' : 'test', 
            'country' : 'test',
            'credit_card_number' : '4242424242424242',
            'cvv' : '111',
            'expiry_month' : 12,
            'expiry_year' : 2019,
            'stripe_id' : 'tok_visa'
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Sorry Name 3 has been already been purchased by another user.')

    """
    check error on trying to pay for empty collection because all artifacts
    have sold
    """
    def test_message_on_all_artifacts_already_sold(self):
        testuser = self.client.login(username='TestName', password='test')
        """ 
        set up a session collection with 1 sold artifact
        """
        session = self.client.session
        collection = {}
        collection[3] = collection.get(3,20)
        session['collection'] = collection
        session.save() 

        response = self.client.post("/checkout/", {
            'full_name' : 'test', 
            'phone_number' : 'test', 
            'street_address1' : 'test', 
            'street_address2' : 'test', 
            'town_or_city' : 'test', 
            'county' : 'test',
            'postcode' : 'test', 
            'country' : 'test',
            'credit_card_number' : '4242424242424242',
            'cvv' : '111',
            'expiry_month' : 12,
            'expiry_year' : 2019,
            'stripe_id' : 'tok_visa'
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Sorry Name 3 has been already been purchased by another user.')
        self.assertEqual(str(messages[1]), 'You have no artifacts in your collection to purchase')
  
    
    """    
    check successful purchase
    """
    def test_message_on_successful_purchase(self):
        testuser = self.client.login(username='TestName', password='test')
        """ 
        set up a session collection with 2 artifacts
        """
        session = self.client.session
        collection = {}
        collection[1] = collection.get(1,{'price' : 20, 'buy_now' : 0 })
        session['collection'] = collection
        session.save() 

        response = self.client.post("/checkout/", {
            'full_name' : 'test', 
            'phone_number' : 'test', 
            'street_address1' : 'test', 
            'street_address2' : 'test', 
            'town_or_city' : 'test', 
            'county' : 'test',
            'postcode' : 'test', 
            'country' : 'test',
            'credit_card_number' : '4242424242424242',
            'cvv' : '111',
            'expiry_month' : 12,
            'expiry_year' : 2019,
            'stripe_id' : 'tok_visa'
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Thank you for purchasing Name 1.')
    
    """
    test buy_all
    """
    
    """
    check the artifact that the user has won is added to the session collection
    """
    
    def test_check_artifacts_added_to_collection(self):
        testuser = self.client.login(username='TestName', password='test')

        """end the auction"""
        auction = get_object_or_404(Auction, pk=1)
        auction.end_date = timezone.now()-timedelta(1)
        auction.save()
        
        response = self.client.get("/checkout/buy_all/", follow=True)
        session = self.client.session

        self.assertRedirects(response, expected_url=reverse('checkout'), status_code=302, target_status_code=200)
        self.assertEqual(session['collection'], {'1': {'price': 5.0, 'buy_now': 0}})


    """
    test buy_one
    """
    
    """
    check the artifact that the user has selected to buy now is added 
    to the session collection
    """
    
    def test_check_artifact_added_to_collection(self):
        testuser = self.client.login(username='TestName', password='test')

        response = self.client.post("/checkout/buy_one/1/1", follow=True)
        session = self.client.session

        self.assertRedirects(response, expected_url=reverse('checkout'), status_code=302, target_status_code=200)
        self.assertEqual(session['collection'], {'1': {'price': 10.0, 'buy_now': '1'}})


    """
    check the artifact that the user has selected to pay for having won auction  
    is added to the session collection
    """
    
    def test_check_won_artifact_added_to_collection(self):
        testuser = self.client.login(username='TestName', password='test')

        """end the auction"""
        auction = get_object_or_404(Auction, pk=1)
        auction.end_date = timezone.now()-timedelta(1)
        auction.save()
        
        response = self.client.post("/checkout/buy_one/1/0", follow=True)
        session = self.client.session

        self.assertRedirects(response, expected_url=reverse('checkout'), status_code=302, target_status_code=200)
        self.assertEqual(session['collection'], {'1' : {'price': 5.0, 'buy_now': '0'}})

        
