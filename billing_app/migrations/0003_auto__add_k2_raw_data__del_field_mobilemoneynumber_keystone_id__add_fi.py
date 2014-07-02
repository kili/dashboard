# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MobileMoneyNumber', fields ['number', 'keystone_id']
        db.delete_unique(u'billing_app_mobilemoneynumber', ['number', 'keystone_id'])

        # Adding model 'k2_raw_data'
        db.create_table(u'billing_app_k2_raw_data', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('business_number', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('transaction_reference', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('internal_transaction_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('transaction_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('sender_phone', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('signature', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'billing_app', ['k2_raw_data'])

        # Deleting field 'MobileMoneyNumber.keystone_id'
        db.delete_column(u'billing_app_mobilemoneynumber', 'keystone_id')

        # Adding field 'MobileMoneyNumber.tenant_id'
        db.add_column(u'billing_app_mobilemoneynumber', 'tenant_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Adding unique constraint on 'MobileMoneyNumber', fields ['number', 'tenant_id']
        db.create_unique(u'billing_app_mobilemoneynumber', ['number', 'tenant_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MobileMoneyNumber', fields ['number', 'tenant_id']
        db.delete_unique(u'billing_app_mobilemoneynumber', ['number', 'tenant_id'])

        # Deleting model 'k2_raw_data'
        db.delete_table(u'billing_app_k2_raw_data')

        # The following code is provided here to aid in writing a correct migration        # Adding field 'MobileMoneyNumber.keystone_id'
        db.add_column(u'billing_app_mobilemoneynumber', 'keystone_id',
                      self.gf('django.db.models.fields.CharField')(max_length=64),
                      keep_default=False)

        # Deleting field 'MobileMoneyNumber.tenant_id'
        db.delete_column(u'billing_app_mobilemoneynumber', 'tenant_id')

        # Adding unique constraint on 'MobileMoneyNumber', fields ['number', 'keystone_id']
        db.create_unique(u'billing_app_mobilemoneynumber', ['number', 'keystone_id'])


    models = {
        u'billing_app.k2_raw_data': {
            'Meta': {'object_name': 'k2_raw_data'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'business_number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sender_phone': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'service_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transaction_reference': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transaction_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'billing_app.mobilemoneynumber': {
            'Meta': {'unique_together': "(('number', 'tenant_id'),)", 'object_name': 'MobileMoneyNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'billing_app.stripecustomer': {
            'Meta': {'unique_together': "(('name', 'keystone_id'),)", 'object_name': 'StripeCustomer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {}),
            'keystone_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']
