# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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


    def backwards(self, orm):
        # Deleting model 'k2_raw_data'
        db.delete_table(u'billing_app_k2_raw_data')


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
        },
    }

    complete_apps = ['billing_app']
