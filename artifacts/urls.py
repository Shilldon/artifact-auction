from django.conf.urls import url
from .views import artifacts_list, display_artifact
from bid.views import get_bid

urlpatterns = [
    url(r'^list/(?P<index_search>\d+)?$', artifacts_list, name="artifacts_list"),
    url(r'^artifact/(?P<id>\d+)$', display_artifact, name="display_artifact"),
    url(r'^list/get_bid', get_bid, name="get_bid"),
    url(r'^artifact/get_bid', get_bid, name="get_bid"),
]
