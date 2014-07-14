# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.conf import settings
from django.db import models
from keystoneclient.v2_0 import client

class Migration(DataMigration):

    def __init__(self, *args, **kwargs):
        super(Migration, self).__init__(*args, **kwargs)
        self.ks_client = client.Client(
            token=settings.KEYSTONE_TOKEN,
            endpoint=settings.KEYSTONE_URL)

    def forwards(self, orm):
        "Write your forwards methods here."
        for card in orm.Card.objects.all():
            card.tenant_id =  self.ks_client.users.get(card.keystone_id).tenantId
            card.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        for card in orm.Card.objects.all():
            card.keystone_id = self.ks_client.tenants.get(card.tenant_id).list_users()[0].id
            card.save()

    models = {
        u'billing_app.card': {
            'Meta': {'unique_together': "(('last4', 'tenant_id'),)", 'object_name': 'Card'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last4': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'tenant_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'keystone_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'billing_app.mobilemoneynumber': {
            'Meta': {'unique_together': "(('number', 'keystone_id'),)", 'object_name': 'MobileMoneyNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keystone_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['billing_app']
    symmetrical = True
