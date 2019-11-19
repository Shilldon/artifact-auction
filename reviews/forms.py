from django import forms
from .models import Review

""" A form to Take a review from the user """
class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        """
        Rating is limited to between 1 and 5
        """
        RATING_CHOICE = [(str(i), str(i)) for i in range (1,6)]
        
        rating = forms.ChoiceField(label='Rating', 
                                   choices=RATING_CHOICE, 
                                   required=True)
        description = forms.CharField(max_length=400, required="True")
        fields = ('rating', 'description', )