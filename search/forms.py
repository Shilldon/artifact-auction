from django import forms
from decimal import Decimal
from artifacts.models import Category


class SearchArtifactsForm(forms.Form):
    
    queryset = Category.objects.all()
    CATEGORY_CHOICES = [ (int(category.id), category.name) for category in queryset]

    default_category_choices = {}
    for category in CATEGORY_CHOICES:
        default_category_choices[category[0]] = True

    TYPE_CHOICES = [
        ('CULTURAL', "Cultural"), 
        ('MEDIA', "Media"),
        ('KNOWLEDGE', "Knowledge"),
        ('DATA', "Data")
    ]
    
    default_type_choices={}
    for type in TYPE_CHOICES:
        default_type_choices[type[0]] = True
    
    name = forms.CharField(label="Name contains:", required=False)
    description = forms.CharField(label="Description contains:", required=False)
    sold = forms.BooleanField(initial=False, required=False)
    in_auction = forms.BooleanField(label="Listed for auction", initial=False, required=False)
    category = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, widget=forms.CheckboxSelectMultiple, required=False, initial=default_category_choices)
    type = forms.MultipleChoiceField(choices=TYPE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False, initial=default_type_choices)
    min_buy_now_price=forms.DecimalField(label="Minimum reserve price", decimal_places=2, required=False)
    max_buy_now_price=forms.DecimalField(label="Maximum reserve price", decimal_places=2, required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data['min_buy_now_price']
        max_price = cleaned_data.get('max_buy_now_price')
        if min_price is None: 
            min_price=Decimal(0.00)
        if max_price is None: 
            max_price=Decimal(0.00)
        if min_price > max_price:
            raise forms.ValidationError(
                "Invalid price range. Maximum price must be more than minimum price."
                )
        
        return min_price, max_price
        
        
