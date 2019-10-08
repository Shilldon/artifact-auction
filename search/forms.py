from django import forms
from artifacts.models import Category

class SearchArtifactsForm(forms.Form):
    
    TYPE_CHOICES = [
        ('CULTURAL', "Cultural"), 
        ('MEDIA', "Media"),
        ('KNOWLEDGE', "Knowledge"),
        ('DATA', "Data")
    ]
    
    name = forms.CharField(label="Name contains:", required=False)
    description = forms.CharField(label="Description contains:", required=False)
    sold = forms.BooleanField(initial=False, required=False)
    in_auction = forms.BooleanField(initial=False, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    type = forms.MultipleChoiceField(choices=TYPE_CHOICES, widget=forms.CheckboxSelectMultiple(), required=False)
    