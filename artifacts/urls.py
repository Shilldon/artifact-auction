from django.conf.urls import url
from .views import artifacts_list, display_artifact

urlpatterns = [
    url(r'^list/', artifacts_list, name="artifacts_list"),
    url(r'^display_artifact/(?P<id>\d+)$', display_artifact, name="display_artifact"),
]
