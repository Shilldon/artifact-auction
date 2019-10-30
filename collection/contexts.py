from django.shortcuts import get_object_or_404
from artifacts.models import Artifact

def collection_contents(request):
    """
    Ensures that the collection contents are available when rendering
    every page
    """
    collection = request.session.get('collection', {})
    total = 0
    purchase = []
    print("collection in context=", collection)
    for id, price in collection.items():
        artifact = get_object_or_404(Artifact, pk=id)
        total += price
        purchase.append({ 'id': id, 'artifact': artifact, 'price' : price })
    
    return {'purchase': purchase, 'total' : total}