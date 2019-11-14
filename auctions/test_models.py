from django import forms
from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Auction
from artifacts.models import Artifact, Category

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
    check model raises error if the artifact is already listed as sold
    """
    def test_end_date_but_no_start_date(self):
        artifact = get_object_or_404(Artifact, pk=1)
        artifact.sold = True
        artifact.save()
        auction = Auction.objects.create(
            artifact = artifact, 
            name = "Auction",             
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1)
        )
        self.assertRaises(ValidationError, auction.clean)    
        with self.assertRaisesMessage(ValidationError, 'That artifact has been sold.'):
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
        