from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Auction, Bid
from artifacts.models import Artifact, Category
from decimal import Decimal
from django.core import mail

class TestAuctionModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        """create an artifact"""
        category = Category(name="test", description="test")
        category.save()
        artifact = Artifact.objects.create(
            name = f'Name { 1 }',
            description = f'Description { 1 }',
            type = 'DATA',
            category = category,
        )

    """
    check model raises error if start_date is less than end_date
    """
    def test_start_date_less_than_end_date(self):
        auction = Auction.objects.create(
            artifact = get_object_or_404(Artifact, pk=1), 
            name = "Auction",             
            start_date = timezone.now(),
            end_date = timezone.now() - timedelta(1)
        )
        with self.assertRaisesMessage(ValidationError, 'Auction end date must be after start date.'):
            auction.clean()
    

    """
    check model raises error if the auction starts in the past 
    """
    def test_start_date_before_now(self):
        artifact = get_object_or_404(Artifact, pk=1)
        artifact.sold = False
        artifact.save()
        auction = Auction.objects.create(
            artifact = artifact, 
            name = "Auction",             
            start_date = timezone.now() - timedelta(1),
            end_date = timezone.now() + timedelta(1)
        )
        self.assertRaises(ValidationError, auction.clean)    
        with self.assertRaisesMessage(ValidationError, 'The start date of the auction may not be in the past.'):
            auction.clean()

class TestBidModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        """create users"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """set the user option to remain anonymous"""
        user.profile.remain_anonymous = True
        user.save()
        
        user2 = User.objects.create_user(username='TestName2', email='test2@…', password='test')
        
        """create artifact"""
        category = Category(name="test", description="test")
        category.save()
        number_of_artifacts = 1
        for artifact_id in range(number_of_artifacts):
            Artifact.objects.create(
                name = f'Name { artifact_id+1 }',
                description = f'Description { artifact_id+1 }',
                type = 'DATA',
                category = category,
                buy_now_price = 1
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
            if bid_id % 2 == 0:
                Bid.objects.create(
                    bid_amount = bid_id+1,
                    bidder = user,
                    auction = auction,
                    time = timezone.now()
                )  
            else:
                Bid.objects.create(
                    bid_amount = bid_id+1,
                    bidder = user2,
                    auction = auction,
                    time = timezone.now()
                )  

    
    """check the buy now price updates after deleting highest bid"""
    def test_buy_now_price_updates(self):
        bids = Bid.objects.all()
        highest_bid = bids.order_by('-bid_amount')[0]
        highest_bid.delete()
        artifact = get_object_or_404(Artifact, pk=1)
        new_buy_now = round(Decimal(4 * 1.2),2)
        self.assertEqual(artifact.buy_now_price,new_buy_now)


    """check the correct bidder is emailed deleting highest bid"""
    def test_email_sent(self):
        bids = Bid.objects.all()
        highest_bid = bids.order_by('-bid_amount')[0]
        highest_bidder = bids.order_by('-bid_amount')[0].bidder
        second_highest_bid = bids.order_by('-bid_amount')[1]
        second_highest_bidder = second_highest_bid.bidder
        highest_bid.delete()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0],  second_highest_bidder.email)    



