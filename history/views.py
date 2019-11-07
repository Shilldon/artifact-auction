from django.shortcuts import render, get_object_or_404
from .models import Historical_Figure, Event

def display_historical_figure(request, id):
    historical_figure = get_object_or_404(Historical_Figure, pk=id)
    events = Event.objects.filter(historical_figure=historical_figure).order_by('sort_year', 'month', 'day')

    artifacts=[]
    for event in events:
        if event.artifact not in artifacts:
            artifacts.append(event.artifact)
       
    return render(request, 'historical_figure.html', { "historical_figure" : historical_figure, "events" : events, "artifacts" : artifacts })

def display_event(request, id):
    event = get_object_or_404(Event, pk=id)
    try:
        other_events = Event.objects.filter(artifact=event.artifact).order_by('sort_year', 'month', 'day')
    except:
        other_events = None
        
    return render(request, 'historical_event.html', { "event" : event, "other_events" : other_events })

