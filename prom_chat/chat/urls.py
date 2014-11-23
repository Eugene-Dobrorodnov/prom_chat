from django.conf.urls import url, patterns

urlpatterns = patterns('chat.views',
    url(r'^$',  'chat_home',  name='home'),
    url(r'^create-channel',   'create_channel', name='create_channel'),
    url(r'^channel/(?P<pk>\d+)/$', 'chat_room', name='chat_room'),
)

