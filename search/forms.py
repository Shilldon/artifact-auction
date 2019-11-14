from django import forms
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from artifacts.models import Category

class SearchArtifactsForm(forms.Form):
    TYPE_CHOICES = [
        ('CULTURAL', "Cultural"), 
        ('MEDIA', "Media"),
        ('KNOWLEDGE', "Knowledge"),
        ('DATA', "Data")
    ]
    
    default_type_choices=[]
    for type in TYPE_CHOICES:
        default_type_choices.append(type[0])
            
    SORT_CHOICES = [
        (1, "Price: Low to High"),
        (2, "Price: High to Low"),
        (3, "Name: A to Z"),
        (4, "Name: Z to A")
    ]

    name = forms.CharField(label="Name contains:", required=False, widget=forms.Textarea(attrs= { 'rows':1, 'cols':1, 'style': 'width:100%; outline:none; resize: none;' }))
    sort_by = forms.ChoiceField(label='Sort by:', choices=SORT_CHOICES, initial=3, required=False)
    description = forms.CharField(label="Description contains:", initial="", required=False, widget=forms.Textarea(attrs= { 'rows':1, 'style': 'width:100%; resize: none;'}))
    sold = forms.BooleanField(initial=False, required=False)
    unsold = forms.BooleanField(initial=False, required=False)
    in_auction = forms.BooleanField(label="Listed for auction", initial=False, required=False)
    not_in_auction = forms.BooleanField(label="Not listed for auction", initial=False, required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, required=True, initial=Category.objects.all())
    type = forms.MultipleChoiceField(choices=TYPE_CHOICES, widget=forms.CheckboxSelectMultiple, required=True, initial=default_type_choices)
    min_buy_now_price=forms.DecimalField(decimal_places=2, required=False,validators=[MinValueValidator(Decimal('0.00'))])
    max_buy_now_price=forms.DecimalField(decimal_places=2, required=False,validators=[MinValueValidator(Decimal('0.00'))])
    
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_buy_now_price')
        max_price = cleaned_data.get('max_buy_now_price')
        if cleaned_data.get("category")==None:
            raise forms.ValidationError(
                "Please select at least one category."
                )            
        if cleaned_data.get("type")==None:
            raise forms.ValidationError(
                "Please select at least one artifact type."
                )            
        if min_price and max_price:
            if min_price > max_price:
                raise forms.ValidationError(
                    "Invalid price range. Maximum price must be more than minimum price."
                    )
            
        else:
            return min_price, max_price

        
