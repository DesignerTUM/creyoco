# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FreeTextVersion'
        db.create_table('exeapp_freetextversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idevice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['exeapp.FreeTextIdevice'])),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(blank=True, default='')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('exeapp', ['FreeTextVersion'])


    def backwards(self, orm):
        # Deleting model 'FreeTextVersion'
        db.delete_table('exeapp_freetextversion')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exeapp.activityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ActivityIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Activity'"})
        },
        'exeapp.appletidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'AppletIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'java_file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'})
        },
        'exeapp.caseactivity': {
            'Meta': {'object_name': 'CaseActivity'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['exeapp.CaseStudyIdevice']"})
        },
        'exeapp.casestudyidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'CaseStudyIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'story': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Case Study'"})
        },
        'exeapp.clozeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ClozeIdevice'},
            'cloze_text': ('exeapp.models.idevices.fields.ClozeTextField', [], {'blank': 'True', 'default': "''"}),
            'description': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Cloze'"})
        },
        'exeapp.commentidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'CommentIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Remark'"})
        },
        'exeapp.dublincore': {
            'Meta': {'object_name': 'DublinCore'},
            'contributors': ('django.db.models.fields.TextField', [], {'max_length': '256', 'blank': 'True'}),
            'coverage': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'exeapp.externalurlidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'ExternalURLIdevice'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'default': "''"})
        },
        'exeapp.feedbackidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'FeedbackIdevice'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'default': "''"})
        },
        'exeapp.freetextidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'FreeTextIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'})
        },
        'exeapp.freetextversion': {
            'Meta': {'object_name': 'FreeTextVersion'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['exeapp.FreeTextIdevice']"})
        },
        'exeapp.genericidevice': {
            'Meta': {'proxy': 'True', '_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'GenericIdevice', 'db_table': "'exeapp_idevice'"}
        },
        'exeapp.glossaryidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'GlossaryIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Glossary'"})
        },
        'exeapp.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'definition': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['exeapp.GlossaryIdevice']"}),
            'title': ('exeapp.models.idevices.fields.RichTextField', [], {'max_length': '100', 'blank': 'True', 'default': "''"})
        },
        'exeapp.idevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Idevice'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'child_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'edit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'idevices'", 'to': "orm['exeapp.Node']"})
        },
        'exeapp.multichoiceidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'MultiChoiceIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'question': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Multiple Choice'"})
        },
        'exeapp.multichoiceoptionidevice': {
            'Meta': {'object_name': 'MultiChoiceOptionIdevice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': "orm['exeapp.MultiChoiceIdevice']"}),
            'option': ('exeapp.models.idevices.fields.MultiChoiceOptionField', [], {'blank': 'True', 'default': "''"}),
            'right_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'exeapp.node': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Node'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['exeapp.Package']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'blank': 'True', 'to': "orm['exeapp.Node']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'exeapp.objectivesidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ObjectivesIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Objectives'"})
        },
        'exeapp.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'backgroundImg': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'backgroundImgTile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shared_packages'", 'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'dublincore': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.DublinCore']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'footer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'footerImg': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Topic'"}),
            'level2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Section'"}),
            'level3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Unit'"}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'resourceDir': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'default'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exeapp.pdfidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'PDFIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'modified_pdf_file': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'page_list': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True', 'default': "''"}),
            'pdf_file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'})
        },
        'exeapp.preknowledgeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'PreknowledgeIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Preknowledge'"})
        },
        'exeapp.readingactivityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ReadingActivityIdevice'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Reading Activity'"}),
            'to_read': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"})
        },
        'exeapp.reflectionidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ReflectionIdevice'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'answer': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Reflection'"})
        },
        'exeapp.rssidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'RSSIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'rss_url': ('exeapp.models.idevices.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'RSS'"})
        },
        'exeapp.tocidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'TOCIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'})
        },
        'exeapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'exeapp.wikipediaidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'WikipediaIdevice'},
            'article_name': ('exeapp.models.idevices.fields.URLField', [], {'max_length': '100', 'blank': 'True', 'default': "''"}),
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.Idevice']", 'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'en'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Wiki Article'"})
        }
    }

    complete_apps = ['exeapp']