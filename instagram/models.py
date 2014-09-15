from django.db import models
from django.core.cache import cache

import urllib2
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
    fetched = models.DateTimeField(null=True)
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

        token, created = cls.objects.get_or_create(userid=properties["userid"], defaults=properties)
        if not created:
            for k, v in properties.items():
                setattr(token, k, v)
            token.save()
        return token


    def save(self, *args, **kwargs):
        if not self.feed_secret:
            self.feed_secret = str(uuid.uuid4())[:13]
        return super(AccessToken, self).save(*args, **kwargs)


    def get_photos(self, method="users/self/feed"):
        cache_key = 'instagram_items_%s_%s'%(self.id, method)
        self.last_time = None
        photos = cache.get(cache_key)

        if not photos:
            url = "https://api.instagram.com/v1/%s?access_token=%s"%(method, self.key)
            start = time.time()
            try:
                conn = urllib2.urlopen(url)
                data = json.loads(conn.read())
            except Exception:
                return []
            self.last_time = time.time() - start
            photos = data["data"]
            cache.set(cache_key, photos, 120)

        for p in photos:
            p["created_time"] = datetime.datetime.utcfromtimestamp(float(p["created_time"]))
            if not p["link"]:
                # private photos don't have public links. link to full-rez image instead.
                p["link"] = p["images"]["standard_resolution"]["url"]

        return photos

    def touch(self):
        self.fetched = datetime.datetime.utcnow()
        self.save()
