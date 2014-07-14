# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_unique('project_billing_raw_statistics_index', ['project_id', 'month', 'meter', 'year'])
        db.create_unique('project_billing_raw_statistics_index', ['from_ts', 'until_ts', 'project_id', 'meter'])
        db.delete_column('project_billing_raw_statistics_index', 'month')
        db.delete_column('project_billing_raw_statistics_index', 'year')

    def backwards(self, orm):
        db.add_column('project_billing_raw_statistics_index', 'month',
                      self.gf('django.db.models.fields.IntegerField')(default=datetime.datetime(2014, 7, 14, 0, 0).month),
                      keep_default=False)
        db.add_column('project_billing_raw_statistics_index', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=datetime.datetime(2014, 7, 14, 0, 0).year),
                      keep_default=False)
        db.delete_unique('project_billing_raw_statistics_index', ['from_ts', 'until_ts', 'project_id', 'meter'])
        db.create_unique('project_billing_raw_statistics_index', ['project_id', 'month', 'meter', 'year'])


    models = {
        u'user_billing.rawstatistics': {
            'Meta': {'object_name': 'RawStatistics', 'db_table': "'project_billing_raw_statistics'"},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'statistics_index': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_billing.RawStatisticsIndex']"})
        },
        u'user_billing.rawstatisticsindex': {
            'Meta': {'unique_together': "[['from_ts', 'until_ts', 'project_id', 'meter']]", 'object_name': 'RawStatisticsIndex', 'db_table': "'project_billing_raw_statistics_index'", 'index_together': "[['from_ts', 'until_ts', 'project_id', 'meter']]"},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'from_ts': ('django.db.models.fields.DateTimeField', [], {}),
            'has_data': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'until_ts': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['user_billing']
