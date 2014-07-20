# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('project_billing_raw_statistics_index', 'from_ts',
                      self.gf('django.db.models.fields.DateTimeField')(null=False),
                      keep_default=False)
        db.add_column('project_billing_raw_statistics_index', 'until_ts',
                      self.gf('django.db.models.fields.DateTimeField')(null=False),
                      keep_default=False)

    def backwards(self, orm):
        db.delete_column('project_billing_raw_statistics_index', 'from_ts')
        db.delete_column('project_billing_raw_statistics_index', 'until_ts')

    models = {
        u'project_billing.rawstatistics': {
            'Meta': {'object_name': 'RawStatistics', 'db_table': "'project_billing_raw_statistics'"},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'statistics_index': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project_billing.RawStatisticsIndex']"})
        },
        u'project_billing.rawstatisticsindex': {
            'Meta': {'unique_together': "[['project_id', 'month', 'meter', 'year']]", 'object_name': 'RawStatisticsIndex', 'db_table': "'project_billing_raw_statistics_index'", 'index_together': "[['project_id', 'month', 'meter', 'year']]"},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'from_ts': ('django.db.models.fields.DateField', [], {'blank': 'False'}),
            'has_data': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'until_ts': ('django.db.models.fields.DateField', [], {'blank': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['project_billing']
