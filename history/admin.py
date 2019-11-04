from django.contrib import admin
from django import forms
from .models import Historical_Figure, Event

import calendar

class EventForm(forms.ModelForm):
    
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range (0,13)]
    month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False, initial=None)
    
    DAY_CHOICES = [(str(i), str(i)) if i > 0 else (str(i), " " ) for i in range (0,32)]
    day = forms.ChoiceField(label='Day', choices=DAY_CHOICES, required=False)
   
    
class EventAdmin(admin.ModelAdmin):
    form = EventForm
    exclude = ('url_description', 'sort_year', 'date')
   
class Historical_FigureAdmin(admin.ModelAdmin):
    model = Historical_Figure
    exclude = ('url_description',)
    
# Register your models here.
admin.site.register(Historical_Figure, Historical_FigureAdmin)
admin.site.register(Event, EventAdmin)