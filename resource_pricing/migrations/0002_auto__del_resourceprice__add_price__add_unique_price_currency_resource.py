# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ResourcePrice'
        db.delete_table('pricing_resource_price')

        # Adding model 'Price'
        db.create_table('pricing_resource_currency_price', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resource_pricing.Currency'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resource_pricing.Resource'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=10)),
        ))
        db.send_create_signal(u'resource_pricing', ['Price'])

        # Adding unique constraint on 'Price', fields ['currency', 'resource']
        db.create_unique('pricing_resource_currency_price', ['currency_id', 'resource_id'])

        # Adding model 'Resource'
        db.create_table('pricing_resource', (
            ('resource_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('resource_type_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'resource_pricing', ['Resource'])


    def backwards(self, orm):
        # Removing unique constraint on 'Price', fields ['currency', 'resource']
        db.delete_unique('pricing_resource_currency_price', ['currency_id', 'resource_id'])

        # Adding model 'ResourcePrice'
        db.create_table('pricing_resource_price', (
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resource_pricing.Currency'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=10)),
            ('resource_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'resource_pricing', ['ResourcePrice'])

        # Deleting model 'Price'
        db.delete_table('pricing_resource_currency_price')

        # Deleting model 'Resource'
        db.delete_table('pricing_resource')


    models = {
        u'resource_pricing.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'pricing_currency'"},
            'currency_iso': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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