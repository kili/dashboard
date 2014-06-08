# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VolumeType'
        db.create_table('pricing_volume_type_resource', (
            ('os_type_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resource_pricing.Resource'])),
        ))
        db.send_create_signal(u'volume', ['VolumeType'])


    def backwards(self, orm):
        # Deleting model 'VolumeType'
        db.delete_table('pricing_volume_type_resource')


    models = {
        u'resource_pricing.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "'pricing_resource'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource_type_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'volume.volumetype': {
            'Meta': {'object_name': 'VolumeType', 'db_table': "'pricing_volume_type_resource'"},
            'os_type_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Resource']"})
        }
    }

    complete_apps = ['volume']