from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from flickr.feeds import PhotoFeed


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', "core.views.index"),

    url(r'^flickr/$', "flickr.views.index"),
    url(r'^flickr/auth/$', "flickr.views.auth"),
    url(r'^flickr/feed/([^/]+)/$', PhotoFeed()),
)
