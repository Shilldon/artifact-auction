from django.conf.urls import url
from .views import add_review, delete_review

urlpatterns = [
    url(r'^review/(?P<id>\d+)$', add_review, name="add_review"),
    url(r'^delete_review/(?P<id>\d+)$', delete_review, name="delete_review"),
    
]
