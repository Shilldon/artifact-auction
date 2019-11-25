from django import forms
from datetime import datetime
from .models import Order
import calendar


class MakePaymentForm(forms.Form):
    """
    A form to take payment from the user.

    Create a list of months from which the user can pick.
    """
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1, 13)]

    """
    Create a list of years from which the user can pick
    """
    YEAR_CHOICES = [(i, i) for i in range(datetime.now().year,
                                          datetime.now().year+15)]

    credit_card_number = forms.CharField(label='Credit card number',
                                         required=False)
    cvv = forms.CharField(label='Security Code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month',
                                     choices=MONTH_CHOICES,
                                     required=False)
    expiry_year = forms.ChoiceField(label='Year',
                                    choices=YEAR_CHOICES,
                                    required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    """
    A form to take order details from the user
    """
    class Meta:
        model = Order
        fields = ('full_name', 'phone_number', 'street_address1',
                  'street_address2', 'town_or_city', 'county',
                  'postcode', 'country'
                  )
