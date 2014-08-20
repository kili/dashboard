# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Threshold'
        db.create_table(u'thresholds_threshold', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=10)),
            ('actions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('down', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'thresholds', ['Threshold'])

        # Adding model 'PassedThreshold'
        db.create_table(u'thresholds_passedthreshold', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('threshold', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thresholds.Threshold'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'thresholds', ['PassedThreshold'])

        # Adding unique constraint on 'PassedThreshold', fields ['project_id', 'threshold']
        db.create_unique(u'thresholds_passedthreshold', ['project_id', 'threshold_id'])

        # Adding model 'ActionQueue'
        db.create_table(u'thresholds_actionqueue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('due_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('kwargs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'thresholds', ['ActionQueue'])


    def backwards(self, orm):
        # Removing unique constraint on 'PassedThreshold', fields ['project_id', 'threshold']
        db.delete_unique(u'thresholds_passedthreshold', ['project_id', 'threshold_id'])

        # Deleting model 'Threshold'
        db.delete_table(u'thresholds_threshold')

        # Deleting model 'PassedThreshold'
        db.delete_table(u'thresholds_passedthreshold')

        # Deleting model 'ActionQueue'
        db.delete_table(u'thresholds_actionqueue')


    models = {
        u'thresholds.actionqueue': {
            'Meta': {'object_name': 'ActionQueue'},
            'due_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'thresholds.passedthreshold': {
            'Meta': {'unique_together': "(('project_id', 'threshold'),)", 'object_name': 'PassedThreshold'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'threshold': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thresholds.Threshold']"})
        },
        u'thresholds.threshold': {
            'Meta': {'object_name': 'Threshold'},
            'actions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'}),
            'down': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'up': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['thresholds']