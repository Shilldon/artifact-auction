from django.conf.urls import url, include
from .views import register, login, logout, view_profile, edit_profile
from accounts import url_reset

urlpatterns=[
    url(r'^register/', register, name='register'),  
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^view_profile/', view_profile, name='view_profile'),
    url(r'^edit_profile/', edit_profile, name='edit_profile'),
    url(r'^password-reset/', include(url_reset))
]