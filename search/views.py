from django.shortcuts import render
from .forms import SearchArtifactsForm
from artifacts.models import Artifact

# Create your views here.
def search_artifacts(request, search_form):
    artifacts = Artifact.objects.all()
    name = search_form['name'].value()
    description = search_form['description'].value()
    sold = search_form['sold'].value()
    in_auction =  search_form['in_auction'].value() 
    category = search_form['category'].value()
    print("sold=", sold)
    artifacts_list = artifacts.filter(description__icontains=description) \
                              .filter(name__icontains=name) \
                              .filter(**filter_by("sold", sold)) \
                              .filter(**filter_by("in_auction", in_auction)) \
                              .filter(**filter_by("category", category))

    return artifacts_list

def filter_by(query_name, query_value):
    print("query name=", query_name)
    if query_value:
        return { query_name : query_value}
    else:
        return {}