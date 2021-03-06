from instagram.models import AccessToken
from flickr.feeds import GeoFeed

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404


class InstagramPhotoFeed(Feed):
    feed_type = GeoFeed
    description_template = 'instagram/_photo.html'

    def get_object(self, request, token_secret):
        token = get_object_or_404(AccessToken, feed_secret = token_secret)
        token.filter_liked = request.REQUEST.get("liked", False)
        token.filter_mine = request.REQUEST.get("mine", False)
        return token
    
    def link(self, obj):
        return "http://feedify.movieos.org/instagram/"
    
    def title(self, obj):
        return u"instagram feed for %s"%obj.username

    def items(self, obj):
        obj.touch()
        if obj.filter_liked:
            return obj.get_photos("users/self/media/liked")
        elif obj.filter_mine:
            return obj.get_photos("users/self/media/recent")
        else:
            return obj.get_photos("users/self/feed")

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

        # https://groups.google.com/forum/?fromgroups=#!topic/instagram-api-developers/ncB18unjqyg
        if isinstance(item["images"]["thumbnail"], dict):
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
        else:
            extra["media:thumbnail"] = dict(
                url = item["images"]["thumbnail"],
            )
            extra["media:content"] = dict(
                url = item["images"]["standard_resolution"],
            )

        return extra
    
