# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_unique('billing_app_mobilemoneynumber', ['number', 'keystone_id'])
        db.rename_column('billing_app_mobilemoneynumber', 'keystone_id', 'tenant_id')
        db.create_unique('billing_app_mobilemoneynumber', ['number'])

    def backwards(self, orm):
        db.delete_unique('billing_app_mobilemoneynumber', ['number'])
        db.rename_column('billing_app_mobilemoneynumber', 'tenant_id', 'keystone_id')
        db.create_unique('billing_app_mobilemoneynumber', ['number', 'keystone_id'])

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
            'Meta': {'object_name': 'MobileMoneyNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']
