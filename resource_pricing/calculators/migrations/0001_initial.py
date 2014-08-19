# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('pricing_instance_flavor_resource', (
            ('os_flavor_id', self.gf('django.db.models.fields.CharField')(primary_key=True, max_length=36)),
            ('resource_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))

        db.create_table('pricing_volume_type_resource', (
            ('os_type_id', self.gf('django.db.models.fields.CharField')(primary_key=True, max_length=36)),
            ('resource_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))

    def backwards(self, orm):
        db.delete_table(u'pricing_instance_flavor_resource')
        db.delete_table(u'pricing_volume_type_resource')


    models = {
        u'calculators.flavor': {
            'Meta': {'object_name': 'Flavor', 'db_table': "'pricing_instance_flavor_resource'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_flavor_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Resource']", 'unique': 'True'})
        },
        u'calculators.volumetype': {
            'Meta': {'object_name': 'VolumeType', 'db_table': "'pricing_volume_type_resource'"},
            'os_type_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Resource']"})
        },
        u'resource_pricing.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "'pricing_resource'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource_type_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['calculators']
