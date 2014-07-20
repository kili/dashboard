# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # work around south bug to delete index which is trying to predict name
        db.rename_column('project_billing_raw_statistics_index', 'project_id', 'user_id')
        db.rename_table('project_billing_raw_statistics_index',
                        'user_billing_raw_statistics_index')
        db.delete_index('user_billing_raw_statistics_index',
                        ['user_id', 'month', 'meter', 'year'])
        db.rename_table('user_billing_raw_statistics_index',
                        'project_billing_raw_statistics_index')
        db.rename_column('project_billing_raw_statistics_index', 'user_id', 'project_id')


        db.delete_unique('project_billing_raw_statistics_index',
                         ['project_id', 'month', 'meter', 'year'])
        db.create_unique('project_billing_raw_statistics_index',
                         ['from_ts', 'until_ts', 'project_id', 'meter'])
        db.delete_column('project_billing_raw_statistics_index', 'month')
        db.delete_column('project_billing_raw_statistics_index', 'year')

        # another workaround for a south bug, also because it's trying to
        # predict the names of indexes (wrongly)
        db.rename_table('project_billing_raw_statistics_index',
                        'user_billing_raw_statistics_index')
        db.delete_index('user_billing_raw_statistics_index', ['fetched'])
        db.delete_index('user_billing_raw_statistics_index', ['billed'])
        db.delete_index('user_billing_raw_statistics_index', ['has_data'])
        db.rename_table('user_billing_raw_statistics_index',
                        'project_billing_rawstatisticsindex')
        db.rename_table('project_billing_raw_statistics',
                        'project_billing_rawstatistics')

    def backwards(self, orm):
        db.rename_table('project_billing_rawstatistics',
                        'project_billing_raw_statistics')
        db.rename_table('project_billing_rawstatisticsindex',
                        'user_billing_raw_statistics_index')
        db.create_index('user_billing_raw_statistics_index', ['has_data'])
        db.create_index('user_billing_raw_statistics_index', ['billed'])
        db.create_index('user_billing_raw_statistics_index', ['fetched'])
        db.rename_table('user_billing_raw_statistics_index',
                        'project_billing_raw_statistics_index')
        db.add_column('project_billing_raw_statistics_index', 'month',
                      self.gf('django.db.models.fields.IntegerField')(default=datetime.datetime(2014, 7, 14, 0, 0).month),
                      keep_default=False)
        db.add_column('project_billing_raw_statistics_index', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=datetime.datetime(2014, 7, 14, 0, 0).year),
                      keep_default=False)
        db.delete_unique('project_billing_raw_statistics_index', ['from_ts', 'until_ts', 'project_id', 'meter'])
        db.create_unique('project_billing_raw_statistics_index', ['project_id', 'month', 'meter', 'year'])


        db.rename_column('project_billing_raw_statistics_index', 'project_id', 'user_id')
        db.rename_table('project_billing_raw_statistics_index',
                        'user_billing_raw_statistics_index')
        db.create_index('user_billing_raw_statistics_index',
                        ['user_id', 'month', 'meter', 'year'])
        db.rename_table('user_billing_raw_statistics_index',
                        'project_billing_raw_statistics_index')
        db.rename_column('project_billing_raw_statistics_index', 'user_id', 'project_id')


    models = {
        u'project_billing.rawstatistics': {
            'Meta': {'object_name': 'RawStatistics', 'db_table': "'project_billing_raw_statistics'"},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'statistics_index': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project_billing.RawStatisticsIndex']"})
        },
        u'project_billing.rawstatisticsindex': {
            'Meta': {'unique_together': "[['from_ts', 'until_ts', 'project_id', 'meter']]", 'object_name': 'RawStatisticsIndex', 'db_table': "'project_billing_raw_statistics_index'", 'index_together': "[['from_ts', 'until_ts', 'project_id', 'meter']]"},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'from_ts': ('django.db.models.fields.DateTimeField', [], {'blank': 'False'}),
            'has_data': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'until_ts': ('django.db.models.fields.DateTimeField', [], {'blank': 'False'})
        }
    }

    complete_apps = ['project_billing']
