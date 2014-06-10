# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RawStatistics'
        db.create_table('user_billing_raw_statistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('insert_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'user_billing', ['RawStatistics'])

        # Adding model 'RawStatisticsIndex'
        db.create_table('user_billing_raw_statistics_index', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('meter', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('fetched', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('raw_statistics', self.gf('django.db.models.fields.related.OneToOneField')(default=-1, to=orm['user_billing.RawStatistics'], unique=True)),
            ('billed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal(u'user_billing', ['RawStatisticsIndex'])

        # Adding unique constraint on 'RawStatisticsIndex', fields ['user_id', 'month', 'meter', 'year']
        db.create_unique('user_billing_raw_statistics_index', ['user_id', 'month', 'meter', 'year'])

        # Adding index on 'RawStatisticsIndex', fields ['user_id', 'month', 'meter', 'year']
        db.create_index('user_billing_raw_statistics_index', ['user_id', 'month', 'meter', 'year'])


    def backwards(self, orm):
        # Removing index on 'RawStatisticsIndex', fields ['user_id', 'month', 'meter', 'year']
        db.delete_index('user_billing_raw_statistics_index', ['user_id', 'month', 'meter', 'year'])

        # Removing unique constraint on 'RawStatisticsIndex', fields ['user_id', 'month', 'meter', 'year']
        db.delete_unique('user_billing_raw_statistics_index', ['user_id', 'month', 'meter', 'year'])

        # Deleting model 'RawStatistics'
        db.delete_table('user_billing_raw_statistics')

        # Deleting model 'RawStatisticsIndex'
        db.delete_table('user_billing_raw_statistics_index')


    models = {
        u'user_billing.rawstatistics': {
            'Meta': {'object_name': 'RawStatistics', 'db_table': "'user_billing_raw_statistics'"},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'user_billing.rawstatisticsindex': {
            'Meta': {'unique_together': "[['user_id', 'month', 'meter', 'year']]", 'object_name': 'RawStatisticsIndex', 'db_table': "'user_billing_raw_statistics_index'", 'index_together': "[['user_id', 'month', 'meter', 'year']]"},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'raw_statistics': ('django.db.models.fields.related.OneToOneField', [], {'default': '-1', 'to': u"orm['user_billing.RawStatistics']", 'unique': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['user_billing']