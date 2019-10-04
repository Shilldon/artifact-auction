from django.conf.urls import url
from .views import artifacts_list, display_artifact, get_bid

urlpatterns = [
    url(r'^list/', artifacts_list, name="artifacts_list"),
    url(r'^artifact/(?P<id>\d+)$', display_artifact, name="display_artifact"),
    url(r'^artifact/get_bid', get_bid, name="get_bid"),
    
]
