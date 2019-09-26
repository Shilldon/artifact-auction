from django.conf.urls import url
from .views import add_to_collection, view_collection

urlpatterns = [
    url(r'^$', view_collection, name='view_collection'),    
    url(r'^add/(?P<id>\d+)/(?P<buy_now>\w+)>', add_to_collection, name="add_to_collection"),
]