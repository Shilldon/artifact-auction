from django.conf.urls import url
from .views import display_owner
from bid.views import get_bid

urlpatterns = [
    url(r'^historical_figure/(?P<id>\d+)$', display_owner, name="display_owner"),
]
