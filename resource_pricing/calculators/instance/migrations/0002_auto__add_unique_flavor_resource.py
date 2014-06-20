# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Flavor', fields ['resource']
        db.create_unique('pricing_instance_flavor_resource', ['resource_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Flavor', fields ['resource']
        db.delete_unique('pricing_instance_flavor_resource', ['resource_id'])


    models = {
        u'instance.flavor': {
            'Meta': {'object_name': 'Flavor', 'db_table': "'pricing_instance_flavor_resource'"},
            'os_flavor_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
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