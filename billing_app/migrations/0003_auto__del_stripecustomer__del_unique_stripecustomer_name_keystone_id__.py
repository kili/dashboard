# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('billing_app_stripecustomer', 'billing_app_card')
        db.delete_unique('billing_app_card', ['is_default', 'keystone_id'])
        db.rename_column('billing_app_card', 'name', 'last4')
        db.rename_column('billing_app_card', 'is_default', 'default')
        db.add_column('billing_app_card', 'tenant_id', models.fields.CharField(max_length=64, db_index=True))
        db.create_unique('billing_app_card', ['last4', 'tenant_id'])

    def backwards(self, orm):
        db.rename_table('billing_app_card', 'billing_app_stripecustomer')
        db.delete_unique('billing_app_stripecustomer', ['last4', 'tenant_id'])
        db.rename_column('billing_app_stripecustomer', 'last4', 'name')
        db.rename_column('billing_app_stripecustomer', 'default', 'is_default')
        db.create_unique('billing_app_stripecustomer', ['is_default', 'keystone_id'])
        db.delete_column('billing_app_stripecustomer', 'tenant_id')

    models = {
        u'billing_app.card': {
            'Meta': {'unique_together': "(('last4', 'tenant_id'),)", 'object_name': 'Card'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last4': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'billing_app.mobilemoneynumber': {
            'Meta': {'unique_together': "(('number', 'keystone_id'),)", 'object_name': 'MobileMoneyNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keystone_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']
