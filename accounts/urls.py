from django.conf.urls import url
from .views import register, login, logout, view_profile, edit_profile

urlpatterns=[
    url(r'^register/', register, name='register'),  
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^view_profile/', view_profile, name='view_profile'),
    url(r'^edit_profile/', edit_profile, name='edit_profile'),
]