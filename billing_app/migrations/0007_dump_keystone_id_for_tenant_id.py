# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for stripecustomer in orm.StripeCustomer.objects.all():
            srtipecustomer.tenant_id = ":)"
            stripecustomer.save()


    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'billing_app.k2rawdata': {
            'Meta': {'object_name': 'K2RawData'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'business_number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'claimed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'keystone_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']
    symmetrical = True
