# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AccessToken'
        db.create_table('instagram_accesstoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('userid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('feed_secret', self.gf('django.db.models.fields.CharField')(unique=True, max_length=13)),
        ))
        db.send_create_signal('instagram', ['AccessToken'])


    def backwards(self, orm):
        
        # Deleting model 'AccessToken'
        db.delete_table('instagram_accesstoken')


    models = {
        'instagram.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'feed_secret': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'userid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['instagram']
