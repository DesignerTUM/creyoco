# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FreeTextIdevice.date_created'
        db.add_column('exeapp_freetextidevice', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime(2014, 9, 4, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FreeTextIdevice.date_created'
        db.delete_column('exeapp_freetextidevice', 'date_created')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exeapp.activityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ActivityIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Activity'"})
        },
        'exeapp.appletidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'AppletIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'java_file': ('filebrowser.fields.FileBrowseField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'exeapp.caseactivity': {
            'Meta': {'object_name': 'CaseActivity'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.CaseStudyIdevice']", 'related_name': "'terms'"})
        },
        'exeapp.casestudyidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'CaseStudyIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'story': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Case Study'"})
        },
        'exeapp.clozeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ClozeIdevice', 'ordering': "('_order',)"},
            'cloze_text': ('exeapp.models.idevices.fields.ClozeTextField', [], {'blank': 'True', 'default': "''"}),
            'description': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Cloze'"})
        },
        'exeapp.commentidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'CommentIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
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
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'ExternalURLIdevice', 'ordering': "('_order',)"},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'default': "''", 'blank': 'True'})
        },
        'exeapp.feedbackidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'FeedbackIdevice', 'ordering': "('_order',)"},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'default': "''", 'blank': 'True'})
        },
        'exeapp.freetextidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'FreeTextIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'exeapp.freetextversion': {
            'Meta': {'object_name': 'FreeTextVersion'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 4, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.FreeTextIdevice']", 'related_name': "'versions'"})
        },
        'exeapp.genericidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'db_table': "'exeapp_idevice'", 'proxy': 'True', 'object_name': 'GenericIdevice', 'ordering': "('_order',)"}
        },
        'exeapp.glossaryidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'GlossaryIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Glossary'"})
        },
        'exeapp.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'definition': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.GlossaryIdevice']", 'related_name': "'terms'"}),
            'title': ('exeapp.models.idevices.fields.RichTextField', [], {'max_length': '100', 'default': "''", 'blank': 'True'})
        },
        'exeapp.idevice': {
            'Meta': {'object_name': 'Idevice', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'child_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'edit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.Node']", 'related_name': "'idevices'"})
        },
        'exeapp.multichoiceidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'MultiChoiceIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'question': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Multiple Choice'"})
        },
        'exeapp.multichoiceoptionidevice': {
            'Meta': {'object_name': 'MultiChoiceOptionIdevice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.MultiChoiceIdevice']", 'related_name': "'options'"}),
            'option': ('exeapp.models.idevices.fields.MultiChoiceOptionField', [], {'blank': 'True', 'default': "''"}),
            'right_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'exeapp.node': {
            'Meta': {'object_name': 'Node', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.Package']", 'related_name': "'nodes'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.Node']", 'null': 'True', 'related_name': "'children'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'exeapp.objectivesidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ObjectivesIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Objectives'"})
        },
        'exeapp.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'backgroundImg': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'backgroundImgTile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'related_name': "'shared_packages'"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'dublincore': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.DublinCore']", 'unique': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'footer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'footerImg': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Topic'"}),
            'level2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Section'"}),
            'level3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Unit'"}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'resourceDir': ('django.db.models.fields.files.FileField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'default'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exeapp.pdfidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'PDFIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'modified_pdf_file': ('django.db.models.fields.FilePathField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'page_list': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "''", 'blank': 'True'}),
            'pdf_file': ('filebrowser.fields.FileBrowseField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'exeapp.preknowledgeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'PreknowledgeIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Preknowledge'"})
        },
        'exeapp.readingactivityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ReadingActivityIdevice', 'ordering': "('_order',)"},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Reading Activity'"}),
            'to_read': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"})
        },
        'exeapp.reflectionidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ReflectionIdevice', 'ordering': "('_order',)"},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'answer': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Reflection'"})
        },
        'exeapp.rssidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'RSSIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'rss_url': ('exeapp.models.idevices.fields.URLField', [], {'max_length': '200', 'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'RSS'"})
        },
        'exeapp.tocidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'TOCIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'exeapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'profile'"})
        },
        'exeapp.wikipediaidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'WikipediaIdevice', 'ordering': "('_order',)"},
            'article_name': ('exeapp.models.idevices.fields.URLField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'en'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Wiki Article'"})
        }
    }

    complete_apps = ['exeapp']