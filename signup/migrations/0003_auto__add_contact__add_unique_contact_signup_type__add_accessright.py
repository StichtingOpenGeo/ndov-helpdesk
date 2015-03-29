# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table('signup_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.SignupQueue'])),
            ('type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal('signup', ['Contact'])

        # Adding unique constraint on 'Contact', fields ['signup', 'type']
        db.create_unique('signup_contact', ['signup_id', 'type'])

        # Adding model 'AccessRight'
        db.create_table('signup_accessright', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signup.SignupQueue'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid_from', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('valid_to', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('signup', ['AccessRight'])


    def backwards(self, orm):
        # Removing unique constraint on 'Contact', fields ['signup', 'type']
        db.delete_unique('signup_contact', ['signup_id', 'type'])

        # Deleting model 'Contact'
        db.delete_table('signup_contact')

        # Deleting model 'AccessRight'
        db.delete_table('signup_accessright')


    models = {
        'signup.accessright': {
            'Meta': {'object_name': 'AccessRight'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.SignupQueue']"}),
            'valid_from': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'valid_to': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        'signup.contact': {
            'Meta': {'unique_together': "(('signup', 'type'),)", 'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'signup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.SignupQueue']"}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        'signup.signupqueue': {
            'Meta': {'object_name': 'SignupQueue'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_requested': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_verified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'signed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['signup']