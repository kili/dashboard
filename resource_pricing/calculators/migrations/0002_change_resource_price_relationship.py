# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('pricing_instance_flavor_resource', 'resource_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resource_pricing.Resource'], unique=True))
        db.rename_column('pricing_instance_flavor_resource', 'resource_id', 'resource_ptr_id')
        db.rename_column('pricing_instance_flavor_resource', 'os_flavor_id', 'os_instance_type_id')
        db.delete_column('pricing_instance_flavor_resource', 'id')
        db.add_column('pricing_instance_flavor_resource', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        db.delete_primary_key('pricing_volume_type_resource')
        db.rename_column('pricing_volume_type_resource', 'os_type_id', 'os_volume_type_id')
        db.create_index('pricing_volume_type_resource', ['os_volume_type_id'], unique=False)
        db.add_column('pricing_volume_type_resource', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)
        db.alter_column('pricing_volume_type_resource', 'resource_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resource_pricing.Resource'], unique=True))
        db.rename_column('pricing_volume_type_resource', 'resource_id', 'resource_ptr_id')

    def backwards(self, orm):
        db.rename_column('pricing_volume_type_resource', 'resource_ptr_id', 'resource_id')
        db.delete_column('pricing_volume_type_resource', u'id')
        db.alter_column('pricing_volume_type_resource', 'os_volume_type_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, db_index=False))
        db.delete_index('pricing_volume_type_resource', ['os_volume_type_id'])
        db.rename_column('pricing_volume_type_resource', 'os_volume_type_id', 'os_type_id')
        db.create_primary_key('pricing_volume_type_resource', ['os_type_id'])

        db.alter_column('pricing_instance_flavor_resource', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))
        db.rename_column('pricing_instance_flavor_resource', 'os_instance_type_id', 'os_flavor_id')
        db.rename_column('pricing_instance_flavor_resource', 'resource_ptr_id', 'resource_id')
        db.alter_column('pricing_instance_flavor_resource', 'resource_id', self.gf('django.db.models.fields.IntegerField')(blank=False))

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
