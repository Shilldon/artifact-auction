import calendar
from django import forms


class EventForm(forms.ModelForm):
    """
    A form to reformat Month and Day field choices for the Event model
    """
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(0, 13)]
    month = forms.ChoiceField(label='Month',
                              choices=MONTH_CHOICES,
                              required=False,
                              initial=None)

    DAY_CHOICES = \
        [(str(i), str(i)) if i > 0 else (str(i), " ") for i in range(0, 32)]
    day = forms.ChoiceField(label='Day', choices=DAY_CHOICES, required=False)
