from decimal import Decimal
from django.core.cache import cache
from django.utils import timezone
from .forms import SearchArtifactsForm
from artifacts.models import Artifact, Category
from auctions.models import Auction


def search_artifacts(request, search_form):
    """
    A view to return a list of artifacts based on search criteria entered
    by the user

    Get list of artifacts from the cache - this will exist if the user
    has previous submitted a search query
    """
    sorted_list = cache.get('sorted_list')
    if search_form.is_valid:
        """
        Get values of the search criteria
        """
        artifacts = Artifact.objects.all()
        name = search_form['name'].value()
        description = search_form['description'].value()
        sold = search_form['sold'].value()
        unsold = search_form['unsold'].value()
        in_auction = search_form['in_auction'].value()
        not_in_auction = search_form['not_in_auction'].value()
        categories = search_form['category'].value()
        artifact_type = search_form['type'].value()
        max_price = search_form['max_buy_now_price'].value()
        min_price = search_form['min_buy_now_price'].value()
        sort_by = search_form["sort_by"].value()

        """
        Convert max and min prices from string to decimal for correct searching
        if blank or 0 return as None to avoid filtering by these criteria
        """

        try:
            max_price = Decimal(max_price.strip(' "'))
        except:
            None
        try:
            min_price = Decimal(min_price.strip(' "'))
        except:
            None

        if max_price == 0:
            max_price = None

        if min_price == 0:
            min_price = None

        artifacts_list = artifacts\
            .filter(**filter_by("description__icontains", description))\
            .filter(**filter_by("name__icontains", name))\
            .filter(**filter_by("sold", sold))\
            .filter(**filter_by("unsold", unsold))\
            .filter(**filter_by("category__id__in", categories))\
            .filter(**filter_by("type__in", artifact_type))\
            .filter(**filter_by("buy_now_price__lte", max_price))\
            .filter(**filter_by("buy_now_price__gte", min_price))

        """
        For in/not_in_auction searches create list of live auctions and further
        filter list based on these auctions
        """
        if in_auction:
            auctions = Auction.objects.filter(end_date__gte=timezone.now())
            artifacts_in_auctions = artifacts_list\
                .filter(id__in=auctions.values('artifact'))
            artifacts_list = artifacts_in_auctions

        if not_in_auction:
            auctions = Auction.objects.filter(end_date__gte=timezone.now())
            artifacts_not_in_auctions = artifacts_list.exclude(
                                                        id__in=auctions
                                                        .values('artifact'))
            artifacts_list = artifacts_not_in_auctions

        """
        If the list is to be sorted determine the sort field or set sort
        alphabetically as default
        """
        if sort_by:
            if int(sort_by) == 1:
                sorted_list = artifacts_list.order_by('buy_now_price')
            elif int(sort_by) == 2:
                sorted_list = artifacts_list.order_by('-buy_now_price')
            elif int(sort_by) == 3:
                sorted_list = artifacts_list.order_by('name')
            elif int(sort_by) == 4:
                sorted_list = artifacts_list.order_by('-name')
        else:
            sorted_list = artifacts_list.order_by('name')

        """
        Send the sorted list to the cache
        """
        cache.set('sorted_list', sorted_list)
        return sorted_list
    else:
        return None


def filter_by(query_name, query_value):
    """
    def to provide filter criteria for the queryset based on values returned
    from the search form
    """
    if query_name == "unsold":
        """
        Unsold search criteria needs to be set as negatived sold property
        """
        if query_value:
            return {"sold": False}
        else:
            return {}
    elif query_value:
        return {query_name: query_value}
    else:
        return {}
