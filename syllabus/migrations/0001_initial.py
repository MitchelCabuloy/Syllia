# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rubric'
        db.create_table(u'syllabus_rubric', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rubric_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('total_rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'syllabus', ['Rubric'])

        # Adding model 'College'
        db.create_table(u'syllabus_college', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('college_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'syllabus', ['College'])

        # Adding model 'Department'
        db.create_table(u'syllabus_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('college', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.College'])),
        ))
        db.send_create_signal(u'syllabus', ['Department'])

        # Adding model 'Syllabus'
        db.create_table(u'syllabus_syllabus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authtools.User'])),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Department'])),
            ('course_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('rubric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Rubric'])),
            ('json_data', self.gf('jsonfield.fields.JSONField')(default={'pk': 0})),
        ))
        db.send_create_signal(u'syllabus', ['Syllabus'])


    def backwards(self, orm):
        # Deleting model 'Rubric'
        db.delete_table(u'syllabus_rubric')

        # Deleting model 'College'
        db.delete_table(u'syllabus_college')

        # Deleting model 'Department'
        db.delete_table(u'syllabus_department')

        # Deleting model 'Syllabus'
        db.delete_table(u'syllabus_syllabus')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'authtools.user': {
            'Meta': {'ordering': "[u'name', u'email']", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'syllabus.college': {
            'Meta': {'object_name': 'College'},
            'college_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'syllabus.department': {
            'Meta': {'object_name': 'Department'},
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.College']"}),
            'department_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'syllabus.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rubric_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'total_rating': ('django.db.models.fields.IntegerField', [], {})
        },
        u'syllabus.syllabus': {
            'Meta': {'object_name': 'Syllabus'},
            'course_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_data': ('jsonfield.fields.JSONField', [], {'default': "{'pk': 0}"}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Rubric']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authtools.User']"})
        }
    }

    complete_apps = ['syllabus']