# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CeilometerFetcherPosition'
        db.create_table('ceilometer_fetcher_position', (
            ('meter_name', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('position', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'ceilometer', ['CeilometerFetcherPosition'])


    def backwards(self, orm):
        # Deleting model 'CeilometerFetcherPosition'
        db.delete_table('ceilometer_fetcher_position')


    models = {
        u'ceilometer.ceilometerfetcherposition': {
            'Meta': {'object_name': 'CeilometerFetcherPosition', 'db_table': "'ceilometer_fetcher_position'"},
            'meter_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'position': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['ceilometer']