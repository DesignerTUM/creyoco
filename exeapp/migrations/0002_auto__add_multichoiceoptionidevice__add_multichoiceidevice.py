# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'MultiChoiceOptionIdevice'
        db.create_table('exeapp_multichoiceoptionidevice', (
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option',
             self.gf('exeapp.models.idevices.fields.MultiChoiceOptionField')(
                 default='', blank=True)),
            ('right_answer',
             self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('idevice', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='options', to=orm['exeapp.MultiChoiceIdevice'])),
        ))
        db.send_create_signal('exeapp', ['MultiChoiceOptionIdevice'])

        # Adding model 'MultiChoiceIdevice'
        db.create_table('exeapp_multichoiceidevice', (
            ('idevice_ptr',
             self.gf('django.db.models.fields.related.OneToOneField')(
                 primary_key=True, unique=True, to=orm['exeapp.Idevice'])),
            ('title', self.gf('django.db.models.fields.CharField')(
                default='Multiple Choice', max_length=100)),
            ('question',
             self.gf('exeapp.models.idevices.fields.RichTextField')(default='',
                                                                    blank=True)),
        ))
        db.send_create_signal('exeapp', ['MultiChoiceIdevice'])


    def backwards(self, orm):
        # Deleting model 'MultiChoiceOptionIdevice'
        db.delete_table('exeapp_multichoiceoptionidevice')

        # Deleting model 'MultiChoiceIdevice'
        db.delete_table('exeapp_multichoiceidevice')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [],
                     {'unique': 'True', 'max_length': '80'}),
            'permissions': (
                'django.db.models.fields.related.ManyToManyField', [],
                {'symmetrical': 'False', 'to': "orm['auth.Permission']",
                 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)",
                     'ordering': "('content_type__app_label', "
                                 "'content_type__model', 'codename')",
                     'object_name': 'Permission'},
            'codename': (
                'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [],
                             {'to': "orm['contenttypes.ContentType']"}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'name': (
                'django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [],
                            {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [],
                      {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [],
                           {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'to': "orm['auth.Group']",
                        'blank': 'True'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'is_active': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'True'}),
            'is_staff': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'False'}),
            'is_superuser': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [],
                           {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [],
                          {'max_length': '30', 'blank': 'True'}),
            'password': (
                'django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': (
                'django.db.models.fields.related.ManyToManyField', [],
                {'symmetrical': 'False', 'to': "orm['auth.Permission']",
                 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [],
                         {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)",
                     'ordering': "('name',)", 'object_name': 'ContentType',
                     'db_table': "'django_content_type'"},
            'app_label': (
                'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'model': (
                'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': (
                'django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exeapp.activityidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'ActivityIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Activity'", 'max_length': '100'})
        },
        'exeapp.appletidevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AppletIdevice',
                     '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'java_file': ('filebrowser.fields.FileBrowseField', [],
                          {'max_length': '100', 'null': 'True',
                           'blank': 'True'})
        },
        'exeapp.caseactivity': {
            'Meta': {'object_name': 'CaseActivity'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [],
                         {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [],
                         {'default': "''", 'blank': 'True'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'terms'",
                         'to': "orm['exeapp.CaseStudyIdevice']"})
        },
        'exeapp.casestudyidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'CaseStudyIdevice',
                     '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'story': ('exeapp.models.idevices.fields.RichTextField', [],
                      {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Case Study'", 'max_length': '100'})
        },
        'exeapp.clozeidevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'ClozeIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'cloze_text': ('exeapp.models.idevices.fields.ClozeTextField', [],
                           {'default': "''", 'blank': 'True'}),
            'description': ('exeapp.models.idevices.fields.RichTextField', [],
                            {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [],
                         {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Cloze'", 'max_length': '100'})
        },
        'exeapp.commentidevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'CommentIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Remark'", 'max_length': '100'})
        },
        'exeapp.dublincore': {
            'Meta': {'object_name': 'DublinCore'},
            'contributors': ('django.db.models.fields.TextField', [],
                             {'max_length': '256', 'blank': 'True'}),
            'coverage': ('django.db.models.fields.CharField', [],
                         {'max_length': '128', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [],
                        {'max_length': '128', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [],
                     {'default': 'datetime.date.today'}),
            'description': (
                'django.db.models.fields.TextField', [], {'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [],
                       {'max_length': '128', 'blank': 'True'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [],
                           {'max_length': '128', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [],
                         {'max_length': '32', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [],
                          {'max_length': '128', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [],
                         {'max_length': '256', 'blank': 'True'}),
            'rights': ('django.db.models.fields.CharField', [],
                       {'max_length': '256', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [],
                       {'max_length': '128', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [],
                        {'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [],
                      {'max_length': '128', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [],
                     {'max_length': '256', 'blank': 'True'})
        },
        'exeapp.externalurlidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'ExternalURLIdevice',
                     '_ormbases': ['exeapp.Idevice']},
            'height': ('django.db.models.fields.PositiveIntegerField', [],
                       {'default': '300'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'url': ('django.db.models.fields.CharField', [],
                    {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'exeapp.feedbackidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'FeedbackIdevice',
                     '_ormbases': ['exeapp.Idevice']},
            'email': ('django.db.models.fields.EmailField', [],
                      {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'subject': ('django.db.models.fields.CharField', [],
                        {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'exeapp.freetextidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'FreeTextIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"})
        },
        'exeapp.genericidevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'GenericIdevice',
                     'proxy': 'True', '_ormbases': ['exeapp.Idevice'],
                     'db_table': "'exeapp_idevice'"}
        },
        'exeapp.glossaryidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'GlossaryIdevice',
                     '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Glossary'", 'max_length': '100'})
        },
        'exeapp.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'definition': ('exeapp.models.idevices.fields.RichTextField', [],
                           {'default': "''", 'blank': 'True'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'terms'",
                         'to': "orm['exeapp.GlossaryIdevice']"}),
            'title': ('exeapp.models.idevices.fields.RichTextField', [],
                      {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        'exeapp.idevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Idevice'},
            '_order': (
                'django.db.models.fields.IntegerField', [], {'default': '0'}),
            'child_type': ('django.db.models.fields.CharField', [],
                           {'max_length': '32', 'blank': 'True'}),
            'edit': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'True'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'idevices'",
                             'to': "orm['exeapp.Node']"})
        },
        'exeapp.multichoiceidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'MultiChoiceIdevice',
                     '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'question': ('exeapp.models.idevices.fields.RichTextField', [],
                         {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Multiple Choice'", 'max_length': '100'})
        },
        'exeapp.multichoiceoptionidevice': {
            'Meta': {'object_name': 'MultiChoiceOptionIdevice'},
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'options'",
                         'to': "orm['exeapp.MultiChoiceIdevice']"}),
            'option': (
                'exeapp.models.idevices.fields.MultiChoiceOptionField', [],
                {'default': "''", 'blank': 'True'}),
            'right_answer': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'False'})
        },
        'exeapp.node': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Node'},
            '_order': (
                'django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'is_root': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'False'}),
            'package': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'nodes'",
                         'to': "orm['exeapp.Package']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [],
                       {'related_name': "'children'",
                        'to': "orm['exeapp.Node']", 'null': 'True',
                        'blank': 'True'}),
            'title': (
                'django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'exeapp.objectivesidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'ObjectivesIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Objectives'", 'max_length': '100'})
        },
        'exeapp.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.CharField', [],
                       {'max_length': '50', 'blank': 'True'}),
            'backgroundImg': ('django.db.models.fields.files.ImageField', [],
                              {'max_length': '100', 'null': 'True',
                               'blank': 'True'}),
            'backgroundImgTile': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [],
                            {'max_length': '256', 'blank': 'True'}),
            'dublincore': ('django.db.models.fields.related.OneToOneField', [],
                           {'unique': 'True',
                            'to': "orm['exeapp.DublinCore']"}),
            'email': ('django.db.models.fields.EmailField', [],
                      {'max_length': '50', 'blank': 'True'}),
            'footer': ('django.db.models.fields.CharField', [],
                       {'max_length': '100', 'blank': 'True'}),
            'footerImg': ('django.db.models.fields.files.ImageField', [],
                          {'max_length': '100', 'null': 'True',
                           'blank': 'True'}),
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'level1': ('django.db.models.fields.CharField', [],
                       {'default': "'Topic'", 'max_length': '20'}),
            'level2': ('django.db.models.fields.CharField', [],
                       {'default': "'Section'", 'max_length': '20'}),
            'level3': ('django.db.models.fields.CharField', [],
                       {'default': "'Unit'", 'max_length': '20'}),
            'license': ('django.db.models.fields.CharField', [],
                        {'max_length': '50', 'blank': 'True'}),
            'resourceDir': ('django.db.models.fields.files.FileField', [],
                            {'max_length': '100', 'null': 'True',
                             'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [],
                      {'default': "'default'", 'max_length': '20'}),
            'title': (
                'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                     {'to': "orm['auth.User']"})
        },
        'exeapp.pdfidevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'PDFIdevice',
                     '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'page_list': ('django.db.models.fields.CharField', [],
                          {'default': "''", 'max_length': '50',
                           'blank': 'True'}),
            'pdf_file': ('filebrowser.fields.FileBrowseField', [],
                         {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'exeapp.preknowledgeidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'PreknowledgeIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Preknowledge'", 'max_length': '100'})
        },
        'exeapp.readingactivityidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'ReadingActivityIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [],
                         {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [],
                         {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Reading Activity'", 'max_length': '100'}),
            'to_read': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'})
        },
        'exeapp.reflectionidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'ReflectionIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [],
                         {'default': "''", 'blank': 'True'}),
            'answer': ('exeapp.models.idevices.fields.FeedbackField', [],
                       {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Reflection'", 'max_length': '100'})
        },
        'exeapp.rssidevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'RSSIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'rss_url': ('exeapp.models.idevices.fields.URLField', [],
                        {'default': "''", 'max_length': '200',
                         'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'RSS'", 'max_length': '100'})
        },
        'exeapp.tocidevice': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'TOCIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"})
        },
        'exeapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [],
                     {'unique': 'True', 'to': "orm['auth.User']"})
        },
        'exeapp.wikipediaidevice': {
            'Meta': {'ordering': "('_order',)",
                     'object_name': 'WikipediaIdevice',
                     '_ormbases': ['exeapp.GenericIdevice']},
            'article_name': ('exeapp.models.idevices.fields.URLField', [],
                             {'default': "''", 'max_length': '100',
                              'blank': 'True'}),
            'content': ('exeapp.models.idevices.fields.RichTextField', [],
                        {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [],
                            {'primary_key': 'True', 'unique': 'True',
                             'to': "orm['exeapp.Idevice']"}),
            'title': ('django.db.models.fields.CharField', [],
                      {'default': "'Wiki Article'", 'max_length': '100'})
        }
    }

    complete_apps = ['exeapp']
