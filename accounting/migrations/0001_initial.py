# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Threshold'
        db.create_table(u'accounting_threshold', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('balance', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('actions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('down', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'accounting', ['Threshold'])

        # Adding model 'PassedThreshold'
        db.create_table(u'accounting_passedthreshold', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('threshold', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.Threshold'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'accounting', ['PassedThreshold'])

        # Adding unique constraint on 'PassedThreshold', fields ['project_id', 'threshold']
        db.create_unique(u'accounting_passedthreshold', ['project_id', 'threshold_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PassedThreshold', fields ['project_id', 'threshold']
        db.delete_unique(u'accounting_passedthreshold', ['project_id', 'threshold_id'])

        # Deleting model 'Threshold'
        db.delete_table(u'accounting_threshold')

        # Deleting model 'PassedThreshold'
        db.delete_table(u'accounting_passedthreshold')


    models = {
        u'accounting.passedthreshold': {
            'Meta': {'unique_together': "(('project_id', 'threshold'),)", 'object_name': 'PassedThreshold'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'threshold': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounting.Threshold']"})
        },
        u'accounting.threshold': {
            'Meta': {'object_name': 'Threshold'},
            'actions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'balance': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'down': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'up': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['accounting']