from django.db import models
from django.conf import settings
from django.core.cache import cache

import urlparse
import urllib
import datetime
import oauth2
import uuid
import json
import time

EXTRAS = "date_upload,date_taken,owner_name,icon_server,original_format,description,geo,tags,machine_tags,o_dims,media,path_alias,url_t,url_s,url_m,url_z,url_l,url_o"

class FlickrException(Exception):
    def __init__(self, code, message):
        self.code = code
        super(FlickrException, self).__init__(message)
    
    def __unicode__(self):
        return u"%s: %s"%(self.code, self.message)

class RequestToken(models.Model):
    key = models.CharField(max_length=100, null=False, blank=False, unique=True)
    secret = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        data = {"oauth_token": self.key, "oauth_token_secret": self.secret}
        return urllib.urlencode(data)

    @classmethod
    def from_string(cls, string):
        data = dict(urlparse.parse_qsl(string))
        token, created = cls.objects.get_or_create(key=data["oauth_token"], defaults=dict(secret = data["oauth_token_secret"]))
        if not created:
            token.secret = data["oauth_token_secret"]
            token.save()
        return token
    
    def token(self):
        return oauth2.Token(self.key, self.secret)


class AccessToken(models.Model):
    key = models.CharField(max_length=100, null=False, blank=False, unique=True)
    secret = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(default=datetime.datetime.utcnow, null=False, blank=False)
    fetched = models.DateTimeField(null=True)
    updated = models.DateTimeField(blank=False, null=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    nsid = models.CharField(max_length=20, null=False, blank=False, unique=True)
    fullname = models.CharField(max_length=100, null=False, blank=False)

    feed_secret = models.CharField(max_length=13, null=False, blank=False, unique=True)

    def __str__(self):
        data = {"oauth_token": self.key, "oauth_token_secret": self.secret}
        return urllib.urlencode(data)

    @classmethod
    def from_string(cls, string):
        data = dict(urlparse.parse_qsl(string))
        properties = dict(
            key = data["oauth_token"],
            secret = data["oauth_token_secret"],
            username=data["username"],
            nsid=data["user_nsid"],
            fullname = data.get("fullname", data["username"]),
            updated = datetime.datetime.utcnow(),
        )

        # remove old IDs for this user.
        cls.objects.filter(nsid=properties["nsid"]).exclude(key=properties["key"]).delete()
        token, created = cls.objects.get_or_create(key=properties["key"], defaults=properties)
        if not created:
            for k, v in properties.items():
                setattr(token, k, v)
            token.save()
        return token

    def token(self):
        return oauth2.Token(self.key, self.secret)
    
    def save(self, *args, **kwargs):
        if not self.feed_secret:
            self.feed_secret = str(uuid.uuid4())[:13]
        return super(AccessToken, self).save(*args, **kwargs)


    def call(self, method, name, **kwargs):
        consumer = oauth2.Consumer(key=settings.FLICKR_API_KEY, secret=settings.FLICKR_API_SECRET)
        client = oauth2.Client(consumer, self.token())

        args = dict(
            method = name,
            format = "json",
            nojsoncallback = "1",
        )
        args.update(kwargs)
        params = urllib.urlencode(args)

        start = time.time()

        if method == "get":
            resp, content = client.request("%s?%s"%(settings.FLICKR_API_URL, params), "GET")
        else:
            resp, content = client.request(settings.FLICKR_API_URL, "POST", body=params)

        self.last_time = time.time() - start

        if resp['status'] != '200':
            raise FlickrException(0, "flickr API error : %s %s"%(resp["status"], content))

        if args["format"] == "json":
            data = json.loads(content)
            if data["stat"] != "ok":
                raise FlickrException(data["code"], data["message"])
            return data
        return content
    
    def recent_photos(self, no_instagram=False, just_friends=False, include_self=False):
        self.last_time = None

        cache_key = 'flickr_items_%s_%s_%s_%s'%(self.id, no_instagram, just_friends, include_self)
        photos = cache.get(cache_key)

        if not photos:
            try:
                response = self.call("get", "flickr.photos.getContactsPhotos", 
                    count = 50,
                    extras = EXTRAS,
                    just_friends = (just_friends and "1" or "0"),
                    include_self = (include_self and "1" or "0"),
                )
                photos = response["photos"]["photo"]
            except FlickrException:
                # don't cache failure
                return []

            def filter_instagram(p):
                mt = p["machine_tags"].split()
                return not "uploaded:by=instagram" in mt
            if no_instagram:
                photos = filter(filter_instagram, photos)
    
            def filter_aaron(p):
                mt = p["machine_tags"].split()
                return not "uploaded:by=parallelflickr" in mt
            photos = filter(filter_aaron, photos)
    
            cache.set(cache_key, photos, 120)

        for p in photos:
            p["description"] = p["description"]["_content"]
            p["link"] = "http://flickr.com/photos/%s/%s"%(p["pathalias"] or p["owner"], p['id'])
            p["upload_date"] = datetime.datetime.utcfromtimestamp(float(p["dateupload"]))
            p["tags"] = p["tags"].split()
        
        return photos

    def touch(self):
        self.fetched = datetime.datetime.utcnow()
        self.save()
        
