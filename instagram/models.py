from django.db import models, IntegrityError
from django.conf import settings
from django.core.cache import cache

import urllib, urllib2
import datetime
import uuid
import json
import time

class InstagramException(Exception):
    def __init__(self, code, message):
        self.code = code
        super(InstagramException, self).__init__(message)
    
    def __unicode__(self):
        return u"%s: %s"%(self.code, self.message)


class AccessToken(models.Model):
    key = models.CharField(max_length=100, null=False, blank=False, unique=True)
    created = models.DateTimeField(default=datetime.datetime.utcnow, null=False, blank=False)
    updated = models.DateTimeField(blank=False, null=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    userid = models.CharField(max_length=20, null=False, blank=False, unique=True)
    feed_secret = models.CharField(max_length=13, null=False, blank=False, unique=True)

    def __str__(self):
        return self.key

    @classmethod
    def from_string(cls, string):
        data = json.loads(string)
        properties = dict(
            key = data["access_token"],
            username = data["user"]["username"],
            userid = data["user"]["id"],
            updated = datetime.datetime.utcnow(),
        )
        try:
            return cls.objects.create(**properties)
        except IntegrityError:
            token = cls.objects.get(key=data["access_token"])
            if token.userid != properties["userid"]:
                raise Exception("token re-used for another user. BAD THING.")

            for k, v in properties.items():
                setattr(token, k, v)
            token.save()
            return token

    def save(self, *args, **kwargs):
        if not self.feed_secret:
            self.feed_secret = str(uuid.uuid4())[:13]
        return super(AccessToken, self).save(*args, **kwargs)

    
    def recent_photos(self):
        cache_key = 'instagram_items_%s'%self.id
        self.last_time = None
        photos = cache.get(cache_key)

        if not photos:
            url = "https://api.instagram.com/v1/users/self/feed?access_token=%s"%self.key
            conn = urllib2.urlopen(url)
            start = time.time()
            data = json.loads(conn.read())
            self.last_time = time.time() - start
            photos = data["data"]
            cache.set(cache_key, photos, 120)

        for p in photos:
            p["created_time"] = datetime.datetime.utcfromtimestamp(float(p["created_time"]))
            if not p["link"]:
                # private photos don't have public links. link to full-rez image instead.
                p["link"] = p["images"]["standard_resolution"]["url"]
        
        return photos

