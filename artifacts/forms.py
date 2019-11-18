from django.core.exceptions import ValidationError
from django import forms

from .models import Artifact
from auctions.models import Auction

class ArtifactRegistrationForm(forms.ModelForm):
    """
    Exclude purchase_price from model form - this field is set on 
    checkout based on whether the purchase is a 'buy now' or final auction bid
    """
    class Meta:
        model = Artifact
        exclude = ['purchase_price',]
       
    def clean_sold(self, *args, **kwargs):
        id = self.instance.id 
        sold = self.cleaned_data.get("sold")
        """
        If the admin sets the artifact status to sold check whether it is 
        listed in an auction. If so throw an error because a sold artifact
        cannot be auctioned.
        """
        if id and sold:
            auction = Auction.objects.filter(artifact__id=id)
            if auction:
                raise ValidationError("That artifact is in a current auction."
                                      " Uncheck 'sold' or delete the auction "
                                      "object.")
        else:
            return sold 
    