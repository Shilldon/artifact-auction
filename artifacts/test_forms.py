from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

from .forms import ArtifactRegistrationForm
from .models import Category, Artifact
from auctions.models import Auction

class TestArtifactRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
    
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """create 2 artifacts"""
        number_of_artifacts = 2
        category = Category(name="test", description="test")
        category.save()
        
        for artifact_id in range(number_of_artifacts):
            artifact = Artifact.objects.create(
                name = f'Name { artifact_id }',
                description = f'Description { artifact_id }',
                type = 'DATA',
                category = category,
                buy_now_price = 1.0,
            )
            
        """create auction"""
        number_of_auctions = 1
        bidder = user 
        for auction_id in range(number_of_auctions):
            artifact = get_object_or_404(Artifact, pk=auction_id+1)
            auction = Auction.objects.create(
                artifact = artifact,
                name = f'Name { auction_id }',
                start_date = timezone.now(),
                end_date = timezone.now() + timedelta(1),

                )
        
    
    """
    Check artifact cannot be created without required fields
    """
    
    def test_artifact_form_required_fields(self):
        form = ArtifactRegistrationForm({'name' : 'test'})
        self.assertFalse(form.is_valid())
        form = ArtifactRegistrationForm({'name' : 'test', 'description' : 'test description'})
        self.assertFalse(form.is_valid())
        form = ArtifactRegistrationForm({'name' : 'test', 'description' : 'test description', 'type' : 'DATA'})
        self.assertFalse(form.is_valid())
        form = ArtifactRegistrationForm({'name' : 'test', 'description' : 'test description', 'type' : 'DATA', 'category' : '1'})
        self.assertFalse(form.is_valid())
        form = ArtifactRegistrationForm({'name' : 'test', 'description' : 'test description', 'type' : 'DATA', 'category' : 1, 'buy_now_price' : 1.00})
        self.assertTrue(form.is_valid())
       
    """
    Check artifact cannot be created if sold or owner but not both, fields are
    entered
    """
    def test_artifact_form_sold_and_owner_required(self):
        form = ArtifactRegistrationForm({'sold' : True, 'name' : 'test', 'description' : 'test description', 'type' : 'DATA', 'category' : 1, 'buy_now_price' : 1.00})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0],'Marked as sold but no owner provided: set owner or uncheck "sold".')
        form = ArtifactRegistrationForm({'owner' : 1, 'name' : 'test', 'description' : 'test description', 'type' : 'DATA', 'category' : 1, 'buy_now_price' : 1.00})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0],'Not marked as sold but owner given: set owner to none or check "sold".')

    """
    Check artifact cannot be marked as sold if it is in an auction
    """
    def test_artifact_cannot_be_sold_if_in_auction(self):
        form = ArtifactRegistrationForm({'owner' : 1, 'sold' : True, 'name' : 'test', 'description' : 'test description', 'type' : 'DATA', 'category' : 1, 'buy_now_price' : 1.00})
        self.assertTrue(form.is_valid())
        instance = form.save()
        auction = Auction.objects.create(
            artifact = get_object_or_404(Artifact, id=instance.pk),
            name = f'Auction Name { 1 }',
            start_date = timezone.now(),
            end_date = timezone.now() + timedelta(1),
        )

        form = ArtifactRegistrationForm({'owner' : 1, 'sold' : True, 'name' : 'test1', 'description' : 'test description', 'type' : 'DATA', 'category' : 1, 'buy_now_price' : 1.00}, instance = instance)
        self.assertEqual(form.errors['sold'][0], "That artifact is in a current auction. Uncheck 'sold' or delete the auction object.")
        self.assertRaises(ValidationError)
    