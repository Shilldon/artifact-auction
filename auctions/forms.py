from django import forms
from .models import Auction, Bid
from artifacts.models import Artifact


class BiddingForm(forms.Form):
    """ A form to take a bid from the user """
    amount_bid = forms.DecimalField(
                                    label="",
                                    max_digits=11,
                                    decimal_places=2,
                                    widget=forms.NumberInput(
                                        attrs={'placeholder': 'Amount Bid'}))


class AuctionForm(forms.ModelForm):
    """
    A form to provide a field of filtered artifacts on creating auction
    instances.

    Filter artifacts and only display artifacts that are not already being
    auctioned and have not been sold.
    """
    auctions = Auction.objects.all()
    artifacts = Artifact.objects.all()\
                        .exclude(pk__in=auctions.values('artifact'))
    artifacts = artifacts.exclude(sold=True)

    artifact = forms.ModelChoiceField(label='Artifact',
                                      queryset=artifacts,
                                      required=True)
