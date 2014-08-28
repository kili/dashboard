# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from nova_wrapper.client import NovaClient


class Migration(DataMigration):

    def forwards(self, orm):
        for instance_type in orm.InstanceType.objects.all():
            instance_type.os_instance_type_id = \
                NovaClient.instance_type_id_to_name(
                    instance_type.os_instance_type_id)
            instance_type.save()

    def backwards(self, orm):
        for instance_type in orm.InstanceType.objects.all():
            instance_type.os_instance_type_id = \
                NovaClient.instance_type_name_to_id(
                    instance_type.os_instance_type_id)
            instance_type.save()

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
    symmetrical = True
