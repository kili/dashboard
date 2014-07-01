# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'StripeCustomer', fields ['name', 'keystone_id']
        db.delete_unique(u'billing_app_stripecustomer', ['name', 'keystone_id'])

        # Deleting field 'StripeCustomer.keystone_id'
        db.delete_column(u'billing_app_stripecustomer', 'keystone_id')

        # Adding field 'StripeCustomer.tenant_id'
        db.add_column(u'billing_app_stripecustomer', 'tenant_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Adding unique constraint on 'StripeCustomer', fields ['name', 'tenant_id']
        db.create_unique(u'billing_app_stripecustomer', ['name', 'tenant_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'StripeCustomer', fields ['name', 'tenant_id']
        db.delete_unique(u'billing_app_stripecustomer', ['name', 'tenant_id'])


        # User chose to not deal with backwards NULL issues for 'StripeCustomer.keystone_id'
        raise RuntimeError("Cannot reverse this migration. 'StripeCustomer.keystone_id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'StripeCustomer.keystone_id'
        db.add_column(u'billing_app_stripecustomer', 'keystone_id',
                      self.gf('django.db.models.fields.CharField')(max_length=64),
                      keep_default=False)

        # Deleting field 'StripeCustomer.tenant_id'
        db.delete_column(u'billing_app_stripecustomer', 'tenant_id')

        # Adding unique constraint on 'StripeCustomer', fields ['name', 'keystone_id']
        db.create_unique(u'billing_app_stripecustomer', ['name', 'keystone_id'])


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
            'Meta': {'unique_together': "(('name', 'tenant_id'),)", 'object_name': 'StripeCustomer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']