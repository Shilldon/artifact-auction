from django.conf.urls import url
from .views import search_artifacts

urlpatterns = [
    url(r'^$', search_artifacts, name="search")
]
