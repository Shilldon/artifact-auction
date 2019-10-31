from django.conf.urls import url
from .views import display_owner, display_event
from bid.views import get_bid

urlpatterns = [
    url(r'^historical_figure/(?P<id>\d+)$', display_owner, name="display_owner"),
    url(r'^historical_event/(?P<id>\d+)$', display_event, name="display_event"),
]
