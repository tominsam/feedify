from flickr.models import AccessToken

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from django.core.cache import cache



class GeoFeed(Atom1Feed):
    def root_attributes(self):
        attrs = super(GeoFeed, self).root_attributes()
        attrs['xmlns:georss'] = 'http://www.georss.org/georss'
        return attrs

    def add_item_elements(self, handler, item):
        super(GeoFeed, self).add_item_elements(handler, item)
        if "latitude" in item and "longitude" in item:
            handler.addQuickElement('georss:point', '%(latitude)s %(longitude)s'%item)



class FlickrPhotoFeed(Feed):
    feed_type = GeoFeed
    description_template = '_flickr_photo.html'

    def get_object(self, request, token_secret):
        self.no_instagram = request.REQUEST.get("no_instagram")
        self.just_friends = request.REQUEST.get("just_friends")
        self.include_self = request.REQUEST.get("include_self")
        return get_object_or_404(AccessToken, feed_secret = token_secret)
    
    def link(self, obj):
        return "http://feedify.movieos.org/flickr/"
    
    def title(self, obj):
        return u"flickr photos for contacts of %s"%obj.fullname

    def items(self, obj):
        cache_key = 'flickr_items_%s_%s_%s_%s'%(obj.id, self.no_instagram, self.just_friends, self.include_self)
        photos = cache.get(cache_key)
        if not photos:
            photos = obj.recent_photos(
                no_instagram=self.no_instagram,
                just_friends=self.just_friends,
                include_self=self.include_self,
            )
            cache.set(cache_key, photos, 60)
        return photos

    def item_title(self, item):
        return u"%s - %s"%(item["ownername"], item["title"])
    
    def item_link(self, item):
        return item["link"]
    
    def item_pubdate(self, item):
        return item["upload_date"]

    def item_extra_kwargs(self, item):
        # template uses this. So it's safe to assume it's inflated.
        if "latitude" in item and "longitude" in item and item["latitude"] and item["longitude"]:
            return {
                "latitude": item["latitude"],
                "longitude": item["longitude"],
            }
        return {}
    
