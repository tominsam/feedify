# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AccessToken.fetched'
        db.add_column('instagram_accesstoken', 'fetched', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'AccessToken.fetched'
        db.delete_column('instagram_accesstoken', 'fetched')


    models = {
        'instagram.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'feed_secret': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'userid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['instagram']
