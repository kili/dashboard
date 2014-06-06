# -*- coding: utf-8 -*-
from django.db import models  # noqa
from south.db import db  # noqa
from south.utils import datetime_utils as datetime  # noqa
from south.v2 import SchemaMigration  # noqa


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StripeCustomer'
        db.create_table(u'billing_app_stripecustomer', (
            (u'id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf(
                'django.db.models.fields.CharField')(max_length=64)),
            ('is_default', self.gf(
                'django.db.models.fields.BooleanField')()),
            ('keystone_id', self.gf(
                'django.db.models.fields.CharField')(max_length=64)),
            ('stripe_customer_id', self.gf(
                'django.db.models.fields.CharField')(unique=True,
                                                     max_length=64)),
        ))
        db.send_create_signal(u'billing_app', ['StripeCustomer'])

        # Adding unique constraint on 'StripeCustomer', fields ['name',
        # 'keystone_id']
        db.create_unique(
            u'billing_app_stripecustomer', ['name', 'keystone_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'StripeCustomer', fields ['name',
        # 'keystone_id']
        db.delete_unique(
            u'billing_app_stripecustomer', ['name', 'keystone_id'])

        # Deleting model 'StripeCustomer'
        db.delete_table(u'billing_app_stripecustomer')

    models = {
        u'billing_app.stripecustomer': {
            'Meta': {'unique_together': "(('name', 'keystone_id'),)",
                     'object_name': 'StripeCustomer'},
            u'id': ('django.db.models.fields.AutoField', [],
                    {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField',
                           [], {}),
            'keystone_id': ('django.db.models.fields.CharField', [],
                            {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [],
                     {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [],
                                   {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']
