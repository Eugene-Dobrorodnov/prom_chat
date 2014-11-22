from django.conf.urls import url, patterns

urlpatterns = patterns('registration.views',
    url(r'^login$',  'login',  name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^signup$', 'signup', name='signup'),
)
