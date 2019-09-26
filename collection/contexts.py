from django.shortcuts import get_object_or_404
from artifacts.models import Artifact

def collection_contents(request):
    """
    Ensures that the collection contents are available when rendering
    every page
    """
    collection = request.session.get('collection', {})
    total = 0
    """
    collection_items = []
    """
    purchase = []
    
    if "purchase" in collection:
        id = collection['purchase']
        artifact = get_object_or_404(Artifact, pk=id)
        purchase = {'id' : id, 'artifact' : artifact}
        total = artifact.price
    """
    for id, in_collection in collection.items():
        artifact = get_object_or_404(Artifact, pk=id)
        total += artifact.price
        collection_items.append({'id': id, 'artifact': artifact})
    """
    
    return {'purchase': purchase, 'total' : total}