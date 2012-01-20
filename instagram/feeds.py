from instagram.models import AccessToken
from flickr.feeds import GeoFeed

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404


class InstagramPhotoFeed(Feed):
    feed_type = GeoFeed
    description_template = 'instagram/_photo.html'

    def get_object(self, request, token_secret):
        return get_object_or_404(AccessToken, feed_secret = token_secret)
    
    def link(self, obj):
        return "http://feedify.movieos.org/instagram/"
    
    def title(self, obj):
        return u"instagram feed for %s"%obj.username

    def items(self, obj):
        return obj.recent_photos()

    def item_title(self, item):
        try:
            caption = (item["caption"] or {})["text"]
        except KeyError:
            caption = "{no caption}"

        return u"%s - %s"%(item["user"]["full_name"], caption)

    def item_author_name(self, item):
        return item["user"]["full_name"]
    
    
    def item_link(self, item):
        return item["link"]
    
    def item_pubdate(self, item):
        return item["created_time"]

    def item_extra_kwargs(self, item):
        extra = {}
        if "location" in item and item["location"] and "latitude" in item["location"] and "longitude" in item["location"]:
            extra["latitude"] = item["location"]["latitude"]
            extra["longiutude"] = item["location"]["longitude"]
        
        extra["media:thumbnail"] = dict(
            url = item["images"]["thumbnail"]["url"],
            width = str(item["images"]["thumbnail"]["width"]),
            height = str(item["images"]["thumbnail"]["height"]),
        )
        extra["media:content"] = dict(
            url = item["images"]["standard_resolution"]["url"],
            width = str(item["images"]["standard_resolution"]["width"]),
            height = str(item["images"]["standard_resolution"]["height"]),
        )

        return extra
    
