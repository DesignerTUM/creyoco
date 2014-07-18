# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PDFIdevice.modified_pdf_file'
        db.add_column('exeapp_pdfidevice', 'modified_pdf_file',
                      self.gf('django.db.models.fields.FilePathField')(blank=True, max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PDFIdevice.modified_pdf_file'
        db.delete_column('exeapp_pdfidevice', 'modified_pdf_file')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exeapp.activityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ActivityIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Activity'"})
        },
        'exeapp.appletidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'AppletIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'java_file': ('filebrowser.fields.FileBrowseField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'})
        },
        'exeapp.caseactivity': {
            'Meta': {'object_name': 'CaseActivity'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['exeapp.CaseStudyIdevice']"})
        },
        'exeapp.casestudyidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'CaseStudyIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'story': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Case Study'"})
        },
        'exeapp.clozeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ClozeIdevice', 'ordering': "('_order',)"},
            'cloze_text': ('exeapp.models.idevices.fields.ClozeTextField', [], {'blank': 'True', 'default': "''"}),
            'description': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Cloze'"})
        },
        'exeapp.commentidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'CommentIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Remark'"})
        },
        'exeapp.dublincore': {
            'Meta': {'object_name': 'DublinCore'},
            'contributors': ('django.db.models.fields.TextField', [], {'blank': 'True', 'max_length': '256'}),
            'coverage': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'creator': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '32'}),
            'publisher': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'relation': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'rights': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'source': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'subject': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'})
        },
        'exeapp.externalurlidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'ExternalURLIdevice', 'ordering': "('_order',)"},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'default': "''"})
        },
        'exeapp.feedbackidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'FeedbackIdevice', 'ordering': "('_order',)"},
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '50', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'default': "''"})
        },
        'exeapp.freetextidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'FreeTextIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'})
        },
        'exeapp.genericidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'db_table': "'exeapp_idevice'", 'proxy': 'True', 'object_name': 'GenericIdevice', 'ordering': "('_order',)"}
        },
        'exeapp.glossaryidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'GlossaryIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Glossary'"})
        },
        'exeapp.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'definition': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['exeapp.GlossaryIdevice']"}),
            'title': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'max_length': '100', 'default': "''"})
        },
        'exeapp.idevice': {
            'Meta': {'object_name': 'Idevice', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'child_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '32'}),
            'edit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'idevices'", 'to': "orm['exeapp.Node']"})
        },
        'exeapp.multichoiceidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'MultiChoiceIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
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
            'Meta': {'object_name': 'Node', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['exeapp.Package']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['exeapp.Node']", 'related_name': "'children'", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'exeapp.objectivesidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ObjectivesIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Objectives'"})
        },
        'exeapp.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'backgroundImg': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'backgroundImgTile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'related_name': "'shared_packages'"}),
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'dublincore': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.DublinCore']", 'unique': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '50'}),
            'footer': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'footerImg': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Topic'"}),
            'level2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Section'"}),
            'level3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Unit'"}),
            'license': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'resourceDir': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'default'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exeapp.pdfidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'object_name': 'PDFIdevice', 'ordering': "('_order',)"},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'modified_pdf_file': ('django.db.models.fields.FilePathField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'page_list': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'default': "''"}),
            'pdf_file': ('filebrowser.fields.FileBrowseField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'})
        },
        'exeapp.preknowledgeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'PreknowledgeIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Preknowledge'"})
        },
        'exeapp.readingactivityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ReadingActivityIdevice', 'ordering': "('_order',)"},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Reading Activity'"}),
            'to_read': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"})
        },
        'exeapp.reflectionidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'ReflectionIdevice', 'ordering': "('_order',)"},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'answer': ('exeapp.models.idevices.fields.FeedbackField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Reflection'"})
        },
        'exeapp.rssidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'RSSIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'rss_url': ('exeapp.models.idevices.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'RSS'"})
        },
        'exeapp.tocidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'TOCIdevice', 'ordering': "('_order',)"},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'})
        },
        'exeapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'to': "orm['auth.User']", 'unique': 'True'})
        },
        'exeapp.wikipediaidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'object_name': 'WikipediaIdevice', 'ordering': "('_order',)"},
            'article_name': ('exeapp.models.idevices.fields.URLField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'blank': 'True', 'default': "''"}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['exeapp.Idevice']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'Wiki Article'"})
        }
    }

    complete_apps = ['exeapp']