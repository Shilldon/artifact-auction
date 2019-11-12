from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache
from .forms import SearchArtifactsForm
from artifacts.models import Artifact, Category
from auctions.models import Auction

# Create your views here.
def search_artifacts(request, search_form):
    sorted_list = cache.get('sorted_list')
    if search_form.is_valid:
        artifacts = Artifact.objects.all()
        name = search_form['name'].value()
        description = search_form['description'].value()
        sold = search_form['sold'].value()
        unsold = search_form['unsold'].value()
        in_auction =  search_form['in_auction'].value() 
        not_in_auction = search_form['not_in_auction'].value()
        categories = search_form['category'].value()
        artifact_type = search_form['type'].value()
        max_price = search_form['max_buy_now_price'].value()
        min_price = search_form['min_buy_now_price'].value()
        sort_by = search_form["sort_by"].value()

        """ set min_price or max_price to none to prevent filter on either of 
        these categories if not entered or entered as 0 on form"""
        try:
            if int(max_price) == 0:
                max_price = None
        except:
            max_price = None
            
        try:
            if int(min_price) == 0:
                min_price = None
        except:
            min_price = None

        if categories:
            category_filter = {'category__id__in' : categories }
        else:
            category_filter = {'category__id' : 0}
            
        if artifact_type:
            type_filter = {'type__in' : artifact_type }
        else:
            type_filter = {'type' : 0}

        artifacts_list = artifacts.filter(**filter_by("description__icontains", description)) \
                                  .filter(**filter_by("name__icontains", name)) \
                                  .filter(**filter_by("sold", sold)) \
                                  .filter(**filter_by("unsold", unsold)) \
                                  .filter(**category_filter) \
                                  .filter(**type_filter) \
                                  .filter(**filter_by("buy_now_price__lte", max_price)) \
                                  .filter(**filter_by("buy_now_price__gte", min_price))
                                  
        if in_auction:
            auctions = Auction.objects.filter(end_date__gte=timezone.now())
            artifacts_in_auctions = artifacts_list.filter(id__in=auctions.values('artifact'))
            artifacts_list = artifacts_in_auctions
        
        if not_in_auction:
            auctions = Auction.objects.filter(end_date__gte=timezone.now())
            artifacts_not_in_auctions = artifacts_list.exclude(id__in=auctions.values('artifact'))
            artifacts_list = artifacts_not_in_auctions

        if sort_by:
            if int(sort_by)==1:
                sorted_list = artifacts_list.order_by('buy_now_price')
            elif int(sort_by)==2:
                sorted_list = artifacts_list.order_by('-buy_now_price')
            elif int(sort_by)==3:
                sorted_list = artifacts_list.order_by('name')
            elif int(sort_by)==4:
                sorted_list = artifacts_list.order_by('-name')
        else:
            sorted_list = artifacts_list.order_by('name')  

        cache.set('sorted_list', sorted_list)
        return sorted_list
    else:
        return None



def filter_by(query_name, query_value):
    if query_name=="unsold":
        if query_value:
            return { "sold" : False }
        else:
            return {}
    elif query_value:
        return { query_name : query_value}
    else:
        return {}
