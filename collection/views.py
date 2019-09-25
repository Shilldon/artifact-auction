from django.shortcuts import render, reverse, redirect, get_object_or_404
from artifacts.models import Artifact

def view_collection(request):
    """A view that renders the collection contents page"""
    collection = request.session.get('collection')
    print("collection ", collection)
    return render(request, "collection.html")

def add_to_collection(request, id):
    collection = request.session.get('collection', {})
    artifact = get_object_or_404(Artifact, pk=id)
    print("collection ", collection)
    if id in collection:
        #return error
        collection = collection
    else:
        artifact.price = artifact.reserve_price
        artifact.save()
        collection[id] = collection.get(id, True)
    
    request.session['collection'] = collection

    return redirect(reverse('artifacts_list'))