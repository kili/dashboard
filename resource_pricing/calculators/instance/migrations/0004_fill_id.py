# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for n, obj in enumerate(orm.Flavor.objects.all()):
            obj.id = n
            obj.save()

        db.delete_primary_key('pricing_instance_flavor_resource')
        db.create_primary_key('pricing_instance_flavor_resource', ['id'])

    def backwards(self, orm):
        "Write your backwards methods here."
        db.delete_primary_key('pricing_instance_flavor_resource')
        db.create_primary_key('pricing_instance_flavor_resource', ['os_flavor_id'])

    models = {
        u'instance.flavor': {
            'Meta': {'object_name': 'Flavor', 'db_table': "'pricing_instance_flavor_resource'"},
            'id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'os_flavor_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'primary_key': 'True', 'db_index': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Resource']", 'unique': 'True'})
        },
        u'resource_pricing.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "'pricing_resource'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource_type_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['instance']
    symmetrical = True
