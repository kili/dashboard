# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table('pricing_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('currency_iso', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'resource_pricing', ['Currency'])

        # Adding model 'ResourcePrice'
        db.create_table('pricing_resource_price', (
            ('resource_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resource_pricing.Currency'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=10)),
        ))
        db.send_create_signal(u'resource_pricing', ['ResourcePrice'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table('pricing_currency')

        # Deleting model 'ResourcePrice'
        db.delete_table('pricing_resource_price')


    models = {
        u'resource_pricing.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'pricing_currency'"},
            'currency_iso': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'resource_pricing.resourceprice': {
            'Meta': {'object_name': 'ResourcePrice', 'db_table': "'pricing_resource_price'"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resource_pricing.Currency']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'}),
            'resource_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['resource_pricing']