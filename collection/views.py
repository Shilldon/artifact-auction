from django.shortcuts import render, reverse, redirect, get_object_or_404
from artifacts.models import Artifact

def view_collection(request):
    """A view that renders the collection contents page"""
    collection = request.session.get('collection')

    return render(request, "collection.html")

def add_to_collection(request, id, buy_now):
    collection = request.session.get('collection', {})
    artifact = get_object_or_404(Artifact, pk=id)

    if int(buy_now)==1:
        artifact.price = artifact.reserve_price
    else:
        artifact.price = artifact.current_bid
    
    artifact.save()
    
    collection["purchase"] = id
        
    request.session['collection'] = collection

    return redirect(reverse('checkout'))