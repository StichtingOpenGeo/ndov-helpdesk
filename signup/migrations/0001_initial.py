# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SignupQueue'
        db.create_table('signup_signupqueue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('representative', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('signed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date_requested', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_uploaded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_verified', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('signup', ['SignupQueue'])


    def backwards(self, orm):
        
        # Deleting model 'SignupQueue'
        db.delete_table('signup_signupqueue')


    models = {
        'signup.signupqueue': {
            'Meta': {'object_name': 'SignupQueue'},
            'business': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_requested': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_verified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'representative': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'signed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['signup']
