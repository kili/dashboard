# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Flavor.id'
        db.add_column('pricing_instance_flavor_resource', 'id',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding index on 'Flavor', fields ['os_flavor_id']
        db.create_index('pricing_instance_flavor_resource', ['os_flavor_id'])


    def backwards(self, orm):
        # Removing index on 'Flavor', fields ['os_flavor_id']
        db.delete_index('pricing_instance_flavor_resource', ['os_flavor_id'])

        # Deleting field 'Flavor.id'
        db.delete_column('pricing_instance_flavor_resource', 'id')


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
