# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MobileMoneyNumber'
        db.create_table(u'billing_app_mobilemoneynumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('keystone_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'billing_app', ['MobileMoneyNumber'])

        # Adding unique constraint on 'MobileMoneyNumber', fields ['number', 'keystone_id']
        db.create_unique(u'billing_app_mobilemoneynumber', ['number', 'keystone_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MobileMoneyNumber', fields ['number', 'keystone_id']
        db.delete_unique(u'billing_app_mobilemoneynumber', ['number', 'keystone_id'])

        # Deleting model 'MobileMoneyNumber'
        db.delete_table(u'billing_app_mobilemoneynumber')


    models = {
        u'billing_app.mobilemoneynumber': {
            'Meta': {'unique_together': "(('number', 'keystone_id'),)", 'object_name': 'MobileMoneyNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keystone_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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