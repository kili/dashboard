# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Currency.currency_iso'
        db.delete_column('pricing_currency', 'currency_iso')

        # Adding field 'Currency.iso'
        db.add_column('pricing_currency', 'iso',
                      self.gf('django.db.models.fields.CharField')(default='USD', max_length=3, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Currency.currency_iso'
        db.add_column('pricing_currency', 'currency_iso',
                      self.gf('django.db.models.fields.CharField')(default='USD', max_length=3),
                      keep_default=False)

        # Deleting field 'Currency.iso'
        db.delete_column('pricing_currency', 'iso')


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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resource_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'resource_type_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['resource_pricing']