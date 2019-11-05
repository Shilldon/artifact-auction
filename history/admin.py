from django.contrib import admin
from .forms import EventForm
from .models import Historical_Figure, Event

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    exclude = ('url_description', 'sort_year', 'date')
   
class Historical_FigureAdmin(admin.ModelAdmin):
    model = Historical_Figure
    exclude = ('url_description',)
    
# Register your models here.
admin.site.register(Historical_Figure, Historical_FigureAdmin)
admin.site.register(Event, EventAdmin)