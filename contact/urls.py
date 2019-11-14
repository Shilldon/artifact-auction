from django.conf.urls import url
from .views import contact

urlpatterns = [
    url(r'^enquiry/$', contact, name="contact"),
]