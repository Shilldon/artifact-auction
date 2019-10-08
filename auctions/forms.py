from django import forms
from .models import Auction
from artifacts.models import Artifact


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Return a string of the format: "firstname lastname (username)"
        return "%s (%s)"%(obj.get_full_name(), obj.username)

class AuctionAdminForm(forms.ModelForm):
    #artifact = UserModelChoiceField(Artifact.objects.exclude(sold=False))
    class Meta:
        model = Auction
        fields = ('artifact',)