# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('pricing_resource', 'resource_pricing_resourcebase')
        db.rename_table('pricing_resource_currency_price', 'resource_pricing_price')
        db.rename_table('pricing_currency', 'resource_pricing_currency')

    def backwards(self, orm):
        db.rename_table('resource_pricing_resourcebase', 'pricing_resource')
        db.rename_table('resource_pricing_price', 'pricing_resource_currency_price')
        db.rename_table('resource_pricing_currency', 'pricing_currency')

    models = {
        u'resource_pricing.currency': {
            'Meta': {'object_name': 'Currency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'})
        },
        u'resource_pricing.price': {
            'Meta': {'unique_together': "(('currency', 'resource'),)", 'object_name': 'Price'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Resource']"})
        },
        u'resource_pricing.resource': {
            'Meta': {'object_name': 'Resource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['resource_pricing']
