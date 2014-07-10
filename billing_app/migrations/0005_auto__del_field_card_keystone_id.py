# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_column(u'billing_app_card', 'keystone_id')

    def backwards(self, orm):
        db.add_column(u'billing_app_card', 'keystone_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, db_index=True),
                      keep_default=False)

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
