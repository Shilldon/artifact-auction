from django import forms
import calendar
from .models import Review

""" Take a review from the user """
class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        RATING_CHOICE = [(str(i), str(i)) for i in range (1,6)]
        
        rating = forms.ChoiceField(label='Rating', choices=RATING_CHOICE, required=True)
        description = forms.CharField(max_length=400, required="True")
        fields = ('rating', 'description', )