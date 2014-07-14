# -*- coding: utf-8 -*-
from django.utils import timezone
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        for index_entry in orm.RawStatisticsIndex.objects.all():
            index_entry.from_ts = datetime.datetime(year=index_entry.year,
                                                    month=index_entry.month,
                                                    day=1,
                                                    hour=0,
                                                    minute=0,
                                                    second=0)
            index_entry.until_ts = datetime.datetime(year=index_entry.year,
                                                     month=index_entry.month + 1,
                                                     day=1,
                                                     hour=0,
                                                     minute=0,
                                                     second=0)
            index_entry.save()

    def backwards(self, orm):
        for index_entry in orm.RawStatisticsIndex.objects.all():
            if not (index_entry.from_ts.year == index_entry.until_ts.year and
                    index_entry.from_ts.month == index_entry.until_ts.month - 1):
                raise Exception('found unexpected data in db, abort migration')
            index_entry.year = index_entry.from_ts.year
            index_entry.month = index_entry.from_ts.month
            index_entry.save()

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
            'from_ts': ('django.db.models.fields.DateTimeField', [], {}),
            'has_data': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'until_ts': ('django.db.models.fields.DateTimeField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['user_billing']
    symmetrical = True
