from django.shortcuts import render, get_object_or_404
from .models import Historical_Figure, Event

def display_historical_figure(request, id):
    """
    A view to pass details of historical figure viewed to the template
    along with the artifact with which they are associated and the events
    linked to that artifact
    """
    historical_figure = get_object_or_404(Historical_Figure, pk=id)
    events = Event.objects.filter(historical_figure=historical_figure)\
                  .order_by('sort_year', 'month', 'day')
    
    """
    Events and historical figures are linked by a common artifact. Create a
    list of all events associated with that artifact.
    """
    artifacts=[]
    for event in events:
        if event.artifact not in artifacts:
            artifacts.append(event.artifact)
       
    return render(
                  request, 
                  'historical_figure.html', 
                  { "historical_figure" : historical_figure, 
                    "events" : events, 
                    "artifacts" : artifacts 
                  })

def display_event(request, id):
    """
    A view to pass details of historical event associated with the relevant
    artifact to the template together with links to all other events
    associated with the artifact
    """    
    event = get_object_or_404(Event, pk=id)
    other_events = Event.objects\
                        .filter(artifact=event.artifact)\
                        .order_by('sort_year', 'month', 'day')\
                        .exclude(pk=id)

    return render(
                    request, 
                    'historical_event.html', 
                    { "event" : event, 
                      "other_events" : other_events 
                        
                    })

