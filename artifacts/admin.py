from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Artifact, Category
from auctions.models import Auction


class ArtifactRegistrationForm(forms.ModelForm):
    def clean(self):
        if self.instance.id:
            sold = self.cleaned_data.get('sold')
            owner = self.cleaned_data.get('owner')
            auction = Auction.objects.filter(artifact__id=self.instance.id)

            if auction and sold and owner:
                raise ValidationError("That artifact is in a current auction. Uncheck 'sold' or delete the auction object.")

class ArtifactAdmin(admin.ModelAdmin):

    form = ArtifactRegistrationForm


    

# Register your models here.
admin.site.register(Artifact, ArtifactAdmin)
admin.site.register(Category)