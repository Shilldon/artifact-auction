from django.shortcuts import get_object_or_404
from artifacts.models import Artifact

def collection_contents(request):
    """
    Ensures that the collection contents are available when rendering
    every page
    """
    collection = request.session.get('collection', [])
    total = 0
    purchase = []
    for id in collection:
        artifact = get_object_or_404(Artifact, pk=id)
        if artifact:
            total += artifact.price
            purchase.append({'id': id, 'artifact': artifact})

    
    return {'purchase': purchase, 'total' : total}