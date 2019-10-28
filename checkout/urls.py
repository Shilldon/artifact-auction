from django.conf.urls import url
from .views import checkout, buy_one, buy_all

urlpatterns = [
    url(r'^$', checkout, name="checkout"),
    url(r'^add/(?P<id>\d+)/(?P<buy_now>\w+)>', buy_one, name="buy_one"),
    url(r'^buy_all/', buy_all, name="buy_all"),    
]