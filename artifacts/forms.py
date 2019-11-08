from django.core.exceptions import ValidationError
from django import forms

from .models import Artifact
from auctions.models import Auction

class ArtifactRegistrationForm(forms.ModelForm):
    class Meta:
        model = Artifact
        fields = '__all__'
       
    def clean_sold(self, *args, **kwargs):
        id = self.instance.id 
        sold = self.cleaned_data.get("sold")
        if id and sold:
            auction = Auction.objects.filter(artifact__id=id)
            if auction:
                raise ValidationError("That artifact is in a current auction. Uncheck 'sold' or delete the auction object.")
        else:
            return sold 
    