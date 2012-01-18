from instagram.models import AccessToken
from flickr.feeds import GeoFeed

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.core.cache import cache


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
        photos = cache.get('instagram_items_%s'%obj.id)
        if not photos:
            photos = obj.recent_photos()
            cache.set('instagram_items_%s'%obj.id, photos, 60)
        
        return photos

    def item_title(self, item):
        try:
            caption = (item["caption"] or {})["text"]
        except KeyError:
            caption = "{no caption}"

        return u"%s - %s"%(item["user"]["full_name"], caption)
    
    def item_link(self, item):
        return item["link"] or "http://feedify.movieos.org/instagram/"
    
    def item_pubdate(self, item):
        return item["created_time"]

    def item_extra_kwargs(self, item):
        if "location" in item and item["location"] and "latitude" in item["location"] and "longitude" in item["location"]:
            return {
                "latitude": item["location"]["latitude"],
                "longitude": item["location"]["longitude"],
            }
        return {}
    
