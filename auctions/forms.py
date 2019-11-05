from django import forms
from .models import Auction
from artifacts.models import Artifact

class AuctionForm(forms.ModelForm):
    
    """only display artifacts that are not already being auctioned and have not been sold"""
    auctions = Auction.objects.all()
    artifacts = Artifact.objects.all().exclude(pk__in=auctions.values('artifact'))
    artifacts = artifacts.exclude(sold=True)

    artifact = forms.ModelChoiceField(label='Artifact', queryset=artifacts, required=True)