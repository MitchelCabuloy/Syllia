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
            ('course_description', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('rubric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Rubric'])),
            ('final_course_output_description', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal(u'syllabus', ['Syllabus'])

        # Adding model 'ClassSchedule'
        db.create_table(u'syllabus_classschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('days', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'syllabus', ['ClassSchedule'])

        # Adding model 'Room'
        db.create_table(u'syllabus_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('room_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'syllabus', ['Room'])

        # Adding model 'Instructor'
        db.create_table(u'syllabus_instructor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('instructor_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'syllabus', ['Instructor'])

        # Adding model 'ELGA'
        db.create_table(u'syllabus_elga', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('elga_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'syllabus', ['ELGA'])

        # Adding model 'LearningOutcome'
        db.create_table(u'syllabus_learningoutcome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('elga', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.ELGA'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'syllabus', ['LearningOutcome'])

        # Adding model 'RequiredOutput'
        db.create_table(u'syllabus_requiredoutput', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('week_due', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'syllabus', ['RequiredOutput'])

        # Adding M2M table for field learning_outcomes on 'RequiredOutput'
        m2m_table_name = db.shorten_name(u'syllabus_requiredoutput_learning_outcomes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('requiredoutput', models.ForeignKey(orm[u'syllabus.requiredoutput'], null=False)),
            ('learningoutcome', models.ForeignKey(orm[u'syllabus.learningoutcome'], null=False))
        ))
        db.create_unique(m2m_table_name, ['requiredoutput_id', 'learningoutcome_id'])

        # Adding model 'Criteria'
        db.create_table(u'syllabus_criteria', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rubric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Rubric'])),
            ('criteria_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('exemplary_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('satisfactory_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('developing_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('beginning_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'syllabus', ['Criteria'])

        # Adding model 'OtherRequirement'
        db.create_table(u'syllabus_otherrequirement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('requirement_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'syllabus', ['OtherRequirement'])

        # Adding model 'GradingSystem'
        db.create_table(u'syllabus_gradingsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('item_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('percentage', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'syllabus', ['GradingSystem'])

        # Adding model 'LearningPlan'
        db.create_table(u'syllabus_learningplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('week_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'syllabus', ['LearningPlan'])

        # Adding M2M table for field learning_outcomes on 'LearningPlan'
        m2m_table_name = db.shorten_name(u'syllabus_learningplan_learning_outcomes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('learningplan', models.ForeignKey(orm[u'syllabus.learningplan'], null=False)),
            ('learningoutcome', models.ForeignKey(orm[u'syllabus.learningoutcome'], null=False))
        ))
        db.create_unique(m2m_table_name, ['learningplan_id', 'learningoutcome_id'])

        # Adding model 'LearningActivity'
        db.create_table(u'syllabus_learningactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('learning_plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.LearningPlan'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'syllabus', ['LearningActivity'])

        # Adding model 'Reference'
        db.create_table(u'syllabus_reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('reference_text', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal(u'syllabus', ['Reference'])

        # Adding model 'ClassPolicy'
        db.create_table(u'syllabus_classpolicy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('syllabus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syllabus.Syllabus'])),
            ('policy_text', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal(u'syllabus', ['ClassPolicy'])


    def backwards(self, orm):
        # Deleting model 'Rubric'
        db.delete_table(u'syllabus_rubric')

        # Deleting model 'College'
        db.delete_table(u'syllabus_college')

        # Deleting model 'Department'
        db.delete_table(u'syllabus_department')

        # Deleting model 'Syllabus'
        db.delete_table(u'syllabus_syllabus')

        # Deleting model 'ClassSchedule'
        db.delete_table(u'syllabus_classschedule')

        # Deleting model 'Room'
        db.delete_table(u'syllabus_room')

        # Deleting model 'Instructor'
        db.delete_table(u'syllabus_instructor')

        # Deleting model 'ELGA'
        db.delete_table(u'syllabus_elga')

        # Deleting model 'LearningOutcome'
        db.delete_table(u'syllabus_learningoutcome')

        # Deleting model 'RequiredOutput'
        db.delete_table(u'syllabus_requiredoutput')

        # Removing M2M table for field learning_outcomes on 'RequiredOutput'
        db.delete_table(db.shorten_name(u'syllabus_requiredoutput_learning_outcomes'))

        # Deleting model 'Criteria'
        db.delete_table(u'syllabus_criteria')

        # Deleting model 'OtherRequirement'
        db.delete_table(u'syllabus_otherrequirement')

        # Deleting model 'GradingSystem'
        db.delete_table(u'syllabus_gradingsystem')

        # Deleting model 'LearningPlan'
        db.delete_table(u'syllabus_learningplan')

        # Removing M2M table for field learning_outcomes on 'LearningPlan'
        db.delete_table(db.shorten_name(u'syllabus_learningplan_learning_outcomes'))

        # Deleting model 'LearningActivity'
        db.delete_table(u'syllabus_learningactivity')

        # Deleting model 'Reference'
        db.delete_table(u'syllabus_reference')

        # Deleting model 'ClassPolicy'
        db.delete_table(u'syllabus_classpolicy')


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
        u'syllabus.classpolicy': {
            'Meta': {'object_name': 'ClassPolicy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'policy_text': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
        },
        u'syllabus.classschedule': {
            'Meta': {'object_name': 'ClassSchedule'},
            'days': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
        },
        u'syllabus.college': {
            'Meta': {'object_name': 'College'},
            'college_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'syllabus.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'beginning_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'criteria_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'developing_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'exemplary_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Rubric']"}),
            'satisfactory_description': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'syllabus.department': {
            'Meta': {'object_name': 'Department'},
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.College']"}),
            'department_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'syllabus.elga': {
            'Meta': {'object_name': 'ELGA'},
            'elga_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
        },
        u'syllabus.gradingsystem': {
            'Meta': {'object_name': 'GradingSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'percentage': ('django.db.models.fields.IntegerField', [], {}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
        },
        u'syllabus.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
        },
        u'syllabus.learningactivity': {
            'Meta': {'object_name': 'LearningActivity'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.LearningPlan']"})
        },
        u'syllabus.learningoutcome': {
            'Meta': {'object_name': 'LearningOutcome'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'elga': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.ELGA']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'syllabus.learningplan': {
            'Meta': {'object_name': 'LearningPlan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_outcomes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['syllabus.LearningOutcome']", 'symmetrical': 'False'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'week_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'syllabus.otherrequirement': {
            'Meta': {'object_name': 'OtherRequirement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirement_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
        },
        u'syllabus.reference': {
            'Meta': {'object_name': 'Reference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_text': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
        },
        u'syllabus.requiredoutput': {
            'Meta': {'object_name': 'RequiredOutput'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_outcomes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['syllabus.LearningOutcome']", 'symmetrical': 'False'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"}),
            'week_due': ('django.db.models.fields.IntegerField', [], {})
        },
        u'syllabus.room': {
            'Meta': {'object_name': 'Room'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'syllabus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Syllabus']"})
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
            'course_description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Department']"}),
            'final_course_output_description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syllabus.Rubric']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authtools.User']"})
        }
    }

    complete_apps = ['syllabus']