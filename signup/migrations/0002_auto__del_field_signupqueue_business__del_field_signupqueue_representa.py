# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'SignupQueue.business'
        db.delete_column('signup_signupqueue', 'business')

        # Deleting field 'SignupQueue.representative'
        db.delete_column('signup_signupqueue', 'representative')

        # Adding field 'SignupQueue.name'
        db.add_column('signup_signupqueue', 'name', self.gf('django.db.models.fields.CharField')(default='-', max_length=75), keep_default=False)

        # Adding field 'SignupQueue.organization'
        db.add_column('signup_signupqueue', 'organization', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'SignupQueue.business'
        raise RuntimeError("Cannot reverse this migration. 'SignupQueue.business' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'SignupQueue.representative'
        raise RuntimeError("Cannot reverse this migration. 'SignupQueue.representative' and its values cannot be restored.")

        # Deleting field 'SignupQueue.name'
        db.delete_column('signup_signupqueue', 'name')

        # Deleting field 'SignupQueue.organization'
        db.delete_column('signup_signupqueue', 'organization')


    models = {
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
            'signed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['signup']
