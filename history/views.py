from django.shortcuts import render, get_object_or_404
from .models import Owner, Event

def display_owner(request, id):
    owner = get_object_or_404(Owner, pk=id)
    events = Event.objects.filter(owner=owner).order_by('sort_year', 'month', 'day')

    artifacts=[]
    for event in events:
        if event.artifact not in artifacts:
            artifacts.append(event.artifact)
       
    return render(request, 'historical_figure.html', { "owner" : owner, "events" : events, "artifacts" : artifacts })

def display_event(request, id):
    event = get_object_or_404(Event, pk=id)

    return render(request, 'historical_event.html', { "event" : event })

