# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('pricing_instance_flavor_resource', 'calculators_instancetype')
        db.rename_table('pricing_volume_type_resource', 'calculators_volumetype')

    def backwards(self, orm):
        db.rename_table('calculators_instancetype', 'pricing_instance_flavor_resource')
        db.rename_table('calculators_volumetype', 'pricing_volume_type_resource')

    models = {
        u'calculators.instancetype': {
            'Meta': {'object_name': 'InstanceType', '_ormbases': [u'resource_pricing.Resource']},
            'os_instance_type_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            u'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['resource_pricing.Resource']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'calculators.volumetype': {
            'Meta': {'object_name': 'VolumeType', '_ormbases': [u'resource_pricing.Resource']},
            'os_volume_type_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            u'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['resource_pricing.Resource']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'resource_pricing.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "'pricing_resource'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['calculators']
