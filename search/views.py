from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import SearchArtifactsForm
from artifacts.models import Artifact, Category

# Create your views here.
def search_artifacts(request, search_form):
    if search_form.is_valid:
        artifacts = Artifact.objects.all()
        name = search_form['name'].value()
        description = search_form['description'].value()
        sold = search_form['sold'].value()
        in_auction =  search_form['in_auction'].value() 
        categories = search_form['category'].value()
        artifact_type = search_form['type'].value()
        max_price = search_form['max_buy_now_price'].value()
        min_price = search_form['min_buy_now_price'].value()

        artifacts_list = artifacts.filter(description__icontains=description) \
                                  .filter(name__icontains=name) \
                                  .filter(**filter_by("sold", sold)) \
                                  .filter(category__id__in=categories) \
                                  .filter(**filter_by("in_auction", in_auction)) \
                                  .filter(type__in=artifact_type) \
                                  .filter(**filter_by("buy_now_price__lte", max_price)) \
                                  .filter(**filter_by("buy_now_price__gte", min_price))
        return artifacts_list

def filter_by(query_name, query_value):
    if query_value:
        return { query_name : query_value}
    else:
        return {}
