from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import SearchArtifactsForm
from artifacts.models import Artifact, Category
from auctions.models import Auction

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
        sort_by = int(search_form["sort_by"].value())


        #.filter(**filter_by("in_auction", in_auction)) \

        artifacts_list = artifacts.filter(description__icontains=description) \
                                  .filter(name__icontains=name) \
                                  .filter(**filter_by("sold", sold)) \
                                  .filter(category__id__in=categories) \
                                  .filter(type__in=artifact_type) \
                                  .filter(**filter_by("buy_now_price__lte", max_price)) \
                                  .filter(**filter_by("buy_now_price__gte", min_price))
        if in_auction:
            auctions = Auction.objects.all()
            artifacts_in_auctions = artifacts_list.filter(id__in=auctions.values('artifact'))
            print(artifacts_in_auctions)
            artifacts_list = artifacts_in_auctions
            
        if sort_by==1:
            print("Sorting price low high")
            sorted_list = artifacts_list.order_by('buy_now_price')
        elif sort_by==2:
            sorted_list = artifacts_list.order_by('-buy_now_price')
            print("Sorting price high low")
        elif sort_by==3:
            sorted_list = artifacts_list.order_by('name')
            print("Sorting name low high")
        elif sort_by==4:
            print("Sorting name high low")
            sorted_list = artifacts_list.order_by('-name')
        print("sorted ", artifacts_list)


        return sorted_list

def filter_by(query_name, query_value):
    if query_value:
        return { query_name : query_value}
    else:
        return {}
