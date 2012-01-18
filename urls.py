from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from flickr.feeds import FlickrPhotoFeed
from instagram.feeds import InstagramPhotoFeed


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', "core.views.index"),

    url(r'^flickr/$', "flickr.views.index"),
    url(r'^flickr/auth/$', "flickr.views.auth"),
    url(r'^flickr/feed/([^/]+)/$', FlickrPhotoFeed()),

    url(r'^instagram/$', "instagram.views.index"),
    url(r'^instagram/auth/$', "instagram.views.auth"),
    url(r'^instagram/feed/([^/]+)/$', InstagramPhotoFeed()),
)
