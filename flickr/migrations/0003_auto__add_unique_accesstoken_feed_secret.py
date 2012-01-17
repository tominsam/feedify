# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'AccessToken', fields ['feed_secret']
        db.create_unique('flickr_accesstoken', ['feed_secret'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AccessToken', fields ['feed_secret']
        db.delete_unique('flickr_accesstoken', ['feed_secret'])


    models = {
        'flickr.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'feed_secret': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'nsid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flickr.requesttoken': {
            'Meta': {'object_name': 'RequestToken'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['flickr']
