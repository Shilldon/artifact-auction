from django.shortcuts import get_object_or_404
from artifacts.models import Artifact

def collection_contents(request):
    """
    Ensures that the collection contents are available when rendering
    every page
    """
    basket = request.session.get('collection', {})
    total = 0
    purchase = []
    for key, value in basket.items():
        artifact = get_object_or_404(Artifact, pk=key)
        total += value['price']
        purchase.append({ 'id': key, 'artifact': artifact, 'price' : value['price'] })
    
    return {'purchase': purchase, 'total' : total}