# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Resource.resource_type_id'
        db.delete_column('pricing_resource', 'resource_type_id')


    def backwards(self, orm):
        # Adding field 'Resource.resource_type_id'
        db.add_column('pricing_resource', 'resource_type_id',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    models = {
        u'resource_pricing.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'pricing_currency'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'})
        },
        u'resource_pricing.price': {
            'Meta': {'unique_together': "(('currency', 'resource'),)", 'object_name': 'Price', 'db_table': "'pricing_resource_currency_price'"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Resource']"})
        },
        u'resource_pricing.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "'pricing_resource'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['resource_pricing']