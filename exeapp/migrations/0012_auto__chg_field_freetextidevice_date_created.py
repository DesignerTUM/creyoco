# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FreeTextIdevice.date_created'
        db.alter_column('exeapp_freetextidevice', 'date_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'FreeTextIdevice.date_created'
        db.alter_column('exeapp_freetextidevice', 'date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 4, 0, 0)))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exeapp.activityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ActivityIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Activity'", 'max_length': '100'})
        },
        'exeapp.appletidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'AppletIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'java_file': ('filebrowser.fields.FileBrowseField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'})
        },
        'exeapp.caseactivity': {
            'Meta': {'object_name': 'CaseActivity'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.CaseStudyIdevice']", 'related_name': "'terms'"})
        },
        'exeapp.casestudyidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'CaseStudyIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'story': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Case Study'", 'max_length': '100'})
        },
        'exeapp.clozeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ClozeIdevice'},
            'cloze_text': ('exeapp.models.idevices.fields.ClozeTextField', [], {'default': "''", 'blank': 'True'}),
            'description': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Cloze'", 'max_length': '100'})
        },
        'exeapp.commentidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'CommentIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Remark'", 'max_length': '100'})
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
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'ExternalURLIdevice'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '200'})
        },
        'exeapp.feedbackidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'FeedbackIdevice'},
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'blank': 'True', 'max_length': '50'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '200'})
        },
        'exeapp.freetextidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'FreeTextIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'exeapp.freetextversion': {
            'Meta': {'object_name': 'FreeTextVersion'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 4, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.FreeTextIdevice']", 'related_name': "'versions'"})
        },
        'exeapp.genericidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'GenericIdevice', 'proxy': 'True', 'db_table': "'exeapp_idevice'"}
        },
        'exeapp.glossaryidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'GlossaryIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Glossary'", 'max_length': '100'})
        },
        'exeapp.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'definition': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.GlossaryIdevice']", 'related_name': "'terms'"}),
            'title': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True', 'max_length': '100'})
        },
        'exeapp.idevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Idevice'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'child_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '32'}),
            'edit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.Node']", 'related_name': "'idevices'"})
        },
        'exeapp.multichoiceidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'MultiChoiceIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'question': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Multiple Choice'", 'max_length': '100'})
        },
        'exeapp.multichoiceoptionidevice': {
            'Meta': {'object_name': 'MultiChoiceOptionIdevice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.MultiChoiceIdevice']", 'related_name': "'options'"}),
            'option': ('exeapp.models.idevices.fields.MultiChoiceOptionField', [], {'default': "''", 'blank': 'True'}),
            'right_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'exeapp.node': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Node'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exeapp.Package']", 'related_name': "'nodes'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['exeapp.Node']", 'null': 'True', 'related_name': "'children'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'exeapp.objectivesidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ObjectivesIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Objectives'", 'max_length': '100'})
        },
        'exeapp.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'backgroundImg': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'backgroundImgTile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'related_name': "'shared_packages'", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'dublincore': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['exeapp.DublinCore']"}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '50'}),
            'footer': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'footerImg': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level1': ('django.db.models.fields.CharField', [], {'default': "'Topic'", 'max_length': '20'}),
            'level2': ('django.db.models.fields.CharField', [], {'default': "'Section'", 'max_length': '20'}),
            'level3': ('django.db.models.fields.CharField', [], {'default': "'Unit'", 'max_length': '20'}),
            'license': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'resourceDir': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exeapp.pdfidevice': {
            'Meta': {'_ormbases': ['exeapp.Idevice'], 'ordering': "('_order',)", 'object_name': 'PDFIdevice'},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'modified_pdf_file': ('django.db.models.fields.FilePathField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'page_list': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '50'}),
            'pdf_file': ('filebrowser.fields.FileBrowseField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'})
        },
        'exeapp.preknowledgeidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'PreknowledgeIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Preknowledge'", 'max_length': '100'})
        },
        'exeapp.readingactivityidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ReadingActivityIdevice'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Reading Activity'", 'max_length': '100'}),
            'to_read': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'})
        },
        'exeapp.reflectionidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'ReflectionIdevice'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'answer': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Reflection'", 'max_length': '100'})
        },
        'exeapp.rssidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'RSSIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'rss_url': ('exeapp.models.idevices.fields.URLField', [], {'default': "''", 'blank': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'RSS'", 'max_length': '100'})
        },
        'exeapp.tocidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'TOCIdevice'},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'exeapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'related_name': "'profile'", 'to': "orm['auth.User']"})
        },
        'exeapp.wikipediaidevice': {
            'Meta': {'_ormbases': ['exeapp.GenericIdevice'], 'ordering': "('_order',)", 'object_name': 'WikipediaIdevice'},
            'article_name': ('exeapp.models.idevices.fields.URLField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Wiki Article'", 'max_length': '100'})
        }
    }

    complete_apps = ['exeapp']