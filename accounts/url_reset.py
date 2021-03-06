from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    #url('^$', password_reset, {'post_reset_redirect': reverse_lazy('password_reset_done')}, name='password_reset'),
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^done/$', password_reset_done, name='password_reset_done'), # uidb creates unique url for the user to change their password (This is what is usually emailed to a user)
    url(r'^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, 
        {'post_reset_redirect': reverse_lazy('password_reset_complete')}, name='password_reset_confirm'),
    url('^complete/$', password_reset_complete, name='password_reset_complete')  
]