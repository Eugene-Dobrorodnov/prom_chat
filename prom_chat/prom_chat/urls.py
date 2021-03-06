from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from common.views import HomeView
from chat.views import ChatView, ChannelDetail, CreateChannelView

import socketio.sdjango
socketio.sdjango.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),

    # Examples:
    # url(r'^$', 'prom_chat.views.home', name='home'),
    # url(r'^prom_chat/', include('prom_chat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url("^socket\.io", include(socketio.sdjango.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/',  include('registration.urls', namespace='user')),
    url(r'^chat/', include('chat.urls', namespace='chat')),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
