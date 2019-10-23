from django.contrib import admin
from django import forms
from .models import Auction
from artifacts.models import Artifact


class AuctionForm(forms.ModelForm):
    
    """only display artifacts that are not already being auctioned or that have not been sold"""
    auctions = Auction.objects.all()
    artifacts = Artifact.objects.all().exclude(pk__in=auctions.values('artifact'))
    artifacts = artifacts.exclude(sold=True)
    #ARTIFACT_CHOICES = [(artifact.id, artifact.name) for artifact in artifacts]

    artifact = forms.ModelChoiceField(label='Artifact', queryset=artifacts, required=True)

class AuctionAdmin(admin.ModelAdmin):
    
    """ prevent admin from changing the artifact related to this auction"""    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('artifact',)
        return self.readonly_fields
    
    form = AuctionForm
    fields = ('artifact', 'start_date', 'end_date')
    
admin.site.register(Auction, AuctionAdmin)

