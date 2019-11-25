from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Category(models.Model):
    """
    Admin can create new categories for artifacts to enable easier searching.
    Categories may include, for example 'clothing, sculpture, artwork etc.'
    """
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Artifact(models.Model):
    """
    Typology provides that artifacts may only belong to one of four types.
    """
    TYPE_CHOICES = [
        ('CULTURAL', "Cultural"),
        ('MEDIA', "Media"),
        ('KNOWLEDGE', "Knowledge"),
        ('DATA', "Data")
    ]

    name = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(default='')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    sold = models.BooleanField(default=False)
    """buy_now - price for which artifact can be purchased right away"""
    buy_now_price = models.DecimalField(max_digits=11, decimal_places=2,
                                        default=0.00)
    """reserve - price under which artifact will not be sold"""
    reserve_price = models.DecimalField(max_digits=11, decimal_places=2,
                                        default=0.00, null=True, blank=True)
    """purchase - price calculated at checkout - hidden field"""
    purchase_price = models.DecimalField(max_digits=11, decimal_places=2,
                                         default=0.00, null=True, blank=True)

    def clean(self):
        """
        Sold Artifacts must be given an owner and artifacts with an owner
        must be marked as sold for display and searching purposes
        """
        if self.owner is None and self.sold is True:
            raise ValidationError('Marked as sold but no owner provided: '
                                  'set owner or uncheck "sold".')
        elif self.sold is False and self.owner is not None:
            raise ValidationError('Not marked as sold but owner given: set '
                                  'owner to none or check "sold".')

        """
        If buy_now and reserve prices are set the buy_now must be more than
        the reserve otherwise users could purchase an artifact for less
        than the reserve price, which defeats the object of having a reserve
        """
        if self.reserve_price and self.reserve_price > self.buy_now_price:
            raise ValidationError('The buy now price must be more than the '
                                  'reserve price.')

    def __str__(self):
        return self.name
