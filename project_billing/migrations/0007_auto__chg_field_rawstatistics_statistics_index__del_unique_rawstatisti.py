# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'RawStatistics', fields ['statistics_index']
        db.delete_unique('project_billing_raw_statistics', ['statistics_index_id'])


        # Changing field 'RawStatistics.statistics_index'
        db.alter_column('project_billing_raw_statistics', 'statistics_index_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_billing.RawStatisticsIndex']))

    def backwards(self, orm):

        # Changing field 'RawStatistics.statistics_index'
        db.alter_column('project_billing_raw_statistics', 'statistics_index_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_billing.RawStatisticsIndex'], unique=True))
        # Adding unique constraint on 'RawStatistics', fields ['statistics_index']
        db.create_unique('project_billing_raw_statistics', ['statistics_index_id'])


    models = {
        u'user_billing.rawstatistics': {
            'Meta': {'object_name': 'RawStatistics', 'db_table': "'project_billing_raw_statistics'"},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'statistics_index': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_billing.RawStatisticsIndex']"})
        },
        u'user_billing.rawstatisticsindex': {
            'Meta': {'unique_together': "[['project_id', 'month', 'meter', 'year']]", 'object_name': 'RawStatisticsIndex', 'db_table': "'project_billing_raw_statistics_index'", 'index_together': "[['project_id', 'month', 'meter', 'year']]"},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'has_data': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['user_billing']