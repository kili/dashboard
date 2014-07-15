# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'K2RawData', fields ['internal_transaction_id']
        db.create_unique(u'billing_app_k2rawdata', ['internal_transaction_id'])

        # Adding unique constraint on 'K2RawData', fields ['transaction_reference']
        db.create_unique(u'billing_app_k2rawdata', ['transaction_reference'])

        db.rename_table('billing_app_k2rawdata', 'billing_app_kopokopotransaction')


    def backwards(self, orm):
        db.rename_table('billing_app_kopokopotransaction', 'billing_app_k2rawdata')

        # Removing unique constraint on 'K2RawData', fields ['transaction_reference']
        db.delete_unique(u'billing_app_k2rawdata', ['transaction_reference'])

        # Removing unique constraint on 'K2RawData', fields ['internal_transaction_id']
        db.delete_unique(u'billing_app_k2rawdata', ['internal_transaction_id'])


    models = {
        u'billing_app.card': {
            'Meta': {'unique_together': "(('last4', 'tenant_id'),)", 'object_name': 'Card'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last4': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'billing_app.k2rawdata': {
            'Meta': {'object_name': 'K2RawData'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'business_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'claimed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_transaction_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'sender_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'service_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transaction_reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'transaction_timestamp': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'billing_app.mobilemoneynumber': {
            'Meta': {'object_name': 'MobileMoneyNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']
