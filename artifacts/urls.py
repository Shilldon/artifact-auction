from django.conf.urls import url
from .views import artifacts_list

urlpatterns = [
    url(r'^$', artifacts_list, name="artifacts"),
]
