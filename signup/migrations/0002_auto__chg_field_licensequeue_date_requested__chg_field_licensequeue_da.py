# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'LicenseQueue.date_requested'
        db.alter_column('signup_signupqueue', 'date_requested', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Changing field 'LicenseQueue.date_verified'
        db.alter_column('signup_signupqueue', 'date_verified', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'LicenseQueue.date_uploaded'
        db.alter_column('signup_signupqueue', 'date_uploaded', self.gf('django.db.models.fields.DateField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'LicenseQueue.date_requested'
        db.alter_column('signup_signupqueue', 'date_requested', self.gf('django.db.models.fields.DateField')())

        # User chose to not deal with backwards NULL issues for 'LicenseQueue.date_verified'
        raise RuntimeError("Cannot reverse this migration. 'LicenseQueue.date_verified' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'LicenseQueue.date_uploaded'
        raise RuntimeError("Cannot reverse this migration. 'LicenseQueue.date_uploaded' and its values cannot be restored.")


    models = {
        'signup.signupqueue': {
            'Meta': {'object_name': 'LicenseQueue'},
            'business': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_requested': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_verified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'representative': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'signed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['signup']
