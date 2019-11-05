from django.core.exceptions import ValidationError
from django import forms

from auctions.models import Auction

class ArtifactRegistrationForm(forms.ModelForm):
    def clean(self):
        if self.instance.id:
            sold = self.cleaned_data.get('sold')
            owner = self.cleaned_data.get('owner')
            auction = Auction.objects.filter(artifact__id=self.instance.id)

            if auction and sold and owner:
                raise ValidationError("That artifact is in a current auction. Uncheck 'sold' or delete the auction object.")
