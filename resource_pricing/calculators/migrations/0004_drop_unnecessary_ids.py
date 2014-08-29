# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_column('calculators_instancetype', 'id')
        db.delete_column('calculators_volumetype', 'id')

    def backwards(self, orm):
        db.add_column('calculators_instancetype', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))
        db.add_column('calculators_volumetype', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

    models = {
        u'calculators.instancetype': {
            'Meta': {'object_name': 'InstanceType', '_ormbases': [u'resource_pricing.ResourceBase']},
            'os_instance_type_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            u'resourcebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['resource_pricing.ResourceBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'calculators.volumetype': {
            'Meta': {'object_name': 'VolumeType', '_ormbases': [u'resource_pricing.ResourceBase']},
            'os_volume_type_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            u'resourcebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['resource_pricing.ResourceBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'resource_pricing.resourcebase': {
            'Meta': {'object_name': 'ResourceBase'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['calculators']
