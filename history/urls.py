from django.conf.urls import url
from .views import display_historical_figure, display_event
from bid.views import get_bid

urlpatterns = [
    url(r'^historical_figure/(?P<id>\d+)$', display_historical_figure, name="display_historical_figure"),
    url(r'^historical_event/(?P<id>\d+)$', display_event, name="display_event"),
]
