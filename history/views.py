from django.shortcuts import render, get_object_or_404
from .models import Owner, Event

def display_owner(request, id):
    owner = get_object_or_404(Owner, pk=id)
    events = Event.objects.filter(owner=owner).order_by('sort_year', 'month', 'day')


    artifacts=[]
    for event in events:
        if event.artifact not in artifacts:
            artifacts.append(event.artifact)
       
    print(events)      
    return render(request, 'historical_figure.html', { "owner" : owner, "events" : events, "artifacts" : artifacts })

