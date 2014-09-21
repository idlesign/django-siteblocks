# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Block', fields ['url', 'alias']
        db.delete_unique(u'siteblocks_block', ['url', 'alias'])

        # Removing index on 'Block', fields ['description']
        db.delete_index(u'siteblocks_block', ['description'])

        # Removing index on 'Block', fields ['url']
        db.delete_index(u'siteblocks_block', ['url'])


    def backwards(self, orm):
        # Adding index on 'Block', fields ['url']
        db.create_index(u'siteblocks_block', ['url'])

        # Adding index on 'Block', fields ['description']
        db.create_index(u'siteblocks_block', ['description'])

        # Adding unique constraint on 'Block', fields ['url', 'alias']
        db.create_unique(u'siteblocks_block', ['url', 'alias'])


    models = {
        u'siteblocks.block': {
            'Meta': {'object_name': 'Block'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['siteblocks']