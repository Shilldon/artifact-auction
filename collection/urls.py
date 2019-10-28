from django.conf.urls import url
from .views import view_collection

urlpatterns = [
    url(r'^$', view_collection, name='view_collection'),    
]