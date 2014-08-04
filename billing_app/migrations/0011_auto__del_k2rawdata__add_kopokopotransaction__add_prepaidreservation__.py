# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'PrePaidReservation'
        db.create_table(u'billing_app_prepaidreservation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('hourly_price', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=10)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=10)),
            ('length', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'billing_app', ['PrePaidReservation'])

        # Adding model 'AssignedReservation'
        db.create_table(u'billing_app_assignedreservation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tenant_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('prepaid_reservation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing_app.PrePaidReservation'])),
        ))
        db.send_create_signal(u'billing_app', ['AssignedReservation'])


    def backwards(self, orm):

        # Deleting model 'PrePaidReservation'
        db.delete_table(u'billing_app_prepaidreservation')

        # Deleting model 'AssignedReservation'
        db.delete_table(u'billing_app_assignedreservation')


    models = {
        u'billing_app.assignedreservation': {
            'Meta': {'object_name': 'AssignedReservation'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prepaid_reservation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing_app.PrePaidReservation']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'billing_app.card': {
            'Meta': {'unique_together': "(('last4', 'tenant_id'),)", 'object_name': 'Card'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last4': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'billing_app.kopokopotransaction': {
            'Meta': {'object_name': 'KopoKopoTransaction'},
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
        },
        u'billing_app.prepaidreservation': {
            'Meta': {'object_name': 'PrePaidReservation'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hourly_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'length': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'})
        }
    }

    complete_apps = ['billing_app']
