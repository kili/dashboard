# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('user_billing_raw_statistics_index', 'project_billing_raw_statistics_index')
        db.rename_table('user_billing_raw_statistics', 'project_billing_raw_statistics')

    def backwards(self, orm):
        db.rename_table('project_billing_raw_statistics_index', 'user_billing_raw_statistics_index')
        db.rename_table('project_billing_raw_statistics', 'user_billing_raw_statistics')

    models = {
        u'user_billing.rawstatistics': {
            'Meta': {'object_name': 'RawStatistics', 'db_table': "'project_billing_raw_statistics'"},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'statistics_index': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['user_billing.RawStatisticsIndex']", 'unique': 'True'})
        },
        u'user_billing.rawstatisticsindex': {
            'Meta': {'unique_together': "[['user_id', 'month', 'meter', 'year']]", 'object_name': 'RawStatisticsIndex', 'db_table': "'project_billing_raw_statistics_index'", 'index_together': "[['user_id', 'month', 'meter', 'year']]"},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'has_data': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['user_billing']
