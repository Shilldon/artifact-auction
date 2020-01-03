from decimal import Decimal
from django.test import TestCase
from artifacts.models import Category, Artifact
from .models import Order, PurchasedArtifact

class TestOrderModel(TestCase):
    """check the Order returns correct value"""
    def test_order_returns_correct_value(self):
        order = Order(
            full_name="Test", 
            phone_number="111",
            county="Test",
            postcode="Test",
            town_or_city="Test",
            street_address1="test",
            street_address2="test",
            country="test",
            date="2011-11-11"
            )
        order.save()
        self.assertEqual(str(order), "Order Number 1 on 2011-11-11 for Test")

class TestPurchasedArtifactModel(TestCase):
    """check Purchased Artifact returns correct value"""
    def test_purchased_artifact_returns_correct_value(self):
        order = Order(
            full_name="Test", 
            phone_number="111",
            county="Test",
            postcode="Test",
            town_or_city="Test",
            street_address1="test",
            street_address2="test",
            country="test",
            date="2011-11-11"
            )
        order.save()
        category = Category(name="test", description="test")
        artifact = Artifact(
            name="test", 
            category=category, 
            description="test", 
            type="DATA", 
            sold=True,
            purchase_price=Decimal(20.00)
        )    
        purchased_artifact = PurchasedArtifact(order=order, artifact=artifact)
        self.assertEqual(str(purchased_artifact), "test @ £20.00")

