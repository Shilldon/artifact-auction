from django import forms

""" Take a bid from the user """
class BiddingForm(forms.Form):
    amount_bid = forms.DecimalField(label="", max_digits=11, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'Amount Bid'}))