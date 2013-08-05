# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('exeapp_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('exeapp', ['UserProfile'])

        # Adding model 'Idevice'
        db.create_table('exeapp_idevice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('edit', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('parent_node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='idevices', to=orm['exeapp.Node'])),
            ('child_type', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('exeapp', ['Idevice'])

        # Adding model 'FreeTextIdevice'
        db.create_table('exeapp_freetextidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['FreeTextIdevice'])

        # Adding model 'ActivityIdevice'
        db.create_table('exeapp_activityidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Activity', max_length=100)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['ActivityIdevice'])

        # Adding model 'GlossaryIdevice'
        db.create_table('exeapp_glossaryidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Glossary', max_length=100)),
        ))
        db.send_create_signal('exeapp', ['GlossaryIdevice'])

        # Adding model 'GlossaryTerm'
        db.create_table('exeapp_glossaryterm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', max_length=100, blank=True)),
            ('definition', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
            ('idevice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='terms', to=orm['exeapp.GlossaryIdevice'])),
        ))
        db.send_create_signal('exeapp', ['GlossaryTerm'])

        # Adding model 'PDFIdevice'
        db.create_table('exeapp_pdfidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('pdf_file', self.gf('filebrowser.fields.FileBrowseField')(max_length=100, null=True, blank=True)),
            ('page_list', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
        ))
        db.send_create_signal('exeapp', ['PDFIdevice'])

        # Adding model 'ReadingActivityIdevice'
        db.create_table('exeapp_readingactivityidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Reading Activity', max_length=100)),
            ('to_read', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
            ('activity', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
            ('feedback', self.gf('exeapp.models.idevices.fields.FeedbackField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['ReadingActivityIdevice'])

        # Adding model 'ReflectionIdevice'
        db.create_table('exeapp_reflectionidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Reflection', max_length=100)),
            ('activity', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
            ('answer', self.gf('exeapp.models.idevices.fields.FeedbackField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['ReflectionIdevice'])

        # Adding model 'TOCIdevice'
        db.create_table('exeapp_tocidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['TOCIdevice'])

        # Adding model 'WikipediaIdevice'
        db.create_table('exeapp_wikipediaidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Wiki Article', max_length=100)),
            ('article_name', self.gf('exeapp.models.idevices.fields.URLField')(default='', max_length=100, blank=True)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['WikipediaIdevice'])

        # Adding model 'ObjectivesIdevice'
        db.create_table('exeapp_objectivesidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Objectives', max_length=100)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['ObjectivesIdevice'])

        # Adding model 'PreknowledgeIdevice'
        db.create_table('exeapp_preknowledgeidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Preknowledge', max_length=100)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['PreknowledgeIdevice'])

        # Adding model 'CommentIdevice'
        db.create_table('exeapp_commentidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Remark', max_length=100)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['CommentIdevice'])

        # Adding model 'FeedbackIdevice'
        db.create_table('exeapp_feedbackidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=50, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
        ))
        db.send_create_signal('exeapp', ['FeedbackIdevice'])

        # Adding model 'RSSIdevice'
        db.create_table('exeapp_rssidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='RSS', max_length=100)),
            ('rss_url', self.gf('exeapp.models.idevices.fields.URLField')(default='', max_length=200, blank=True)),
            ('content', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['RSSIdevice'])

        # Adding model 'ExternalURLIdevice'
        db.create_table('exeapp_externalurlidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=300)),
        ))
        db.send_create_signal('exeapp', ['ExternalURLIdevice'])

        # Adding model 'AppletIdevice'
        db.create_table('exeapp_appletidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('java_file', self.gf('filebrowser.fields.FileBrowseField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('exeapp', ['AppletIdevice'])

        # Adding model 'ClozeIdevice'
        db.create_table('exeapp_clozeidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Cloze', max_length=100)),
            ('description', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
            ('cloze_text', self.gf('exeapp.models.idevices.fields.ClozeTextField')(default='', blank=True)),
            ('feedback', self.gf('exeapp.models.idevices.fields.FeedbackField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['ClozeIdevice'])

        # Adding model 'CaseStudyIdevice'
        db.create_table('exeapp_casestudyidevice', (
            ('idevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.Idevice'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Case Study', max_length=100)),
            ('story', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal('exeapp', ['CaseStudyIdevice'])

        # Adding model 'CaseActivity'
        db.create_table('exeapp_caseactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('exeapp.models.idevices.fields.RichTextField')(default='', blank=True)),
            ('feedback', self.gf('exeapp.models.idevices.fields.FeedbackField')(default='', blank=True)),
            ('idevice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='terms', to=orm['exeapp.CaseStudyIdevice'])),
        ))
        db.send_create_signal('exeapp', ['CaseActivity'])

        # Adding model 'Node'
        db.create_table('exeapp_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['exeapp.Package'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['exeapp.Node'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_root', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('exeapp', ['Node'])

        # Adding model 'DublinCore'
        db.create_table('exeapp_dublincore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('contributors', self.gf('django.db.models.fields.TextField')(max_length=256, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('coverage', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('rights', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal('exeapp', ['DublinCore'])

        # Adding model 'Package'
        db.create_table('exeapp_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('backgroundImg', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('backgroundImgTile', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('footer', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('footerImg', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('style', self.gf('django.db.models.fields.CharField')(default='default', max_length=20)),
            ('resourceDir', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('dublincore', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['exeapp.DublinCore'], unique=True)),
            ('level1', self.gf('django.db.models.fields.CharField')(default='Topic', max_length=20)),
            ('level2', self.gf('django.db.models.fields.CharField')(default='Section', max_length=20)),
            ('level3', self.gf('django.db.models.fields.CharField')(default='Unit', max_length=20)),
        ))
        db.send_create_signal('exeapp', ['Package'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('exeapp_userprofile')

        # Deleting model 'Idevice'
        db.delete_table('exeapp_idevice')

        # Deleting model 'FreeTextIdevice'
        db.delete_table('exeapp_freetextidevice')

        # Deleting model 'ActivityIdevice'
        db.delete_table('exeapp_activityidevice')

        # Deleting model 'GlossaryIdevice'
        db.delete_table('exeapp_glossaryidevice')

        # Deleting model 'GlossaryTerm'
        db.delete_table('exeapp_glossaryterm')

        # Deleting model 'PDFIdevice'
        db.delete_table('exeapp_pdfidevice')

        # Deleting model 'ReadingActivityIdevice'
        db.delete_table('exeapp_readingactivityidevice')

        # Deleting model 'ReflectionIdevice'
        db.delete_table('exeapp_reflectionidevice')

        # Deleting model 'TOCIdevice'
        db.delete_table('exeapp_tocidevice')

        # Deleting model 'WikipediaIdevice'
        db.delete_table('exeapp_wikipediaidevice')

        # Deleting model 'ObjectivesIdevice'
        db.delete_table('exeapp_objectivesidevice')

        # Deleting model 'PreknowledgeIdevice'
        db.delete_table('exeapp_preknowledgeidevice')

        # Deleting model 'CommentIdevice'
        db.delete_table('exeapp_commentidevice')

        # Deleting model 'FeedbackIdevice'
        db.delete_table('exeapp_feedbackidevice')

        # Deleting model 'RSSIdevice'
        db.delete_table('exeapp_rssidevice')

        # Deleting model 'ExternalURLIdevice'
        db.delete_table('exeapp_externalurlidevice')

        # Deleting model 'AppletIdevice'
        db.delete_table('exeapp_appletidevice')

        # Deleting model 'ClozeIdevice'
        db.delete_table('exeapp_clozeidevice')

        # Deleting model 'CaseStudyIdevice'
        db.delete_table('exeapp_casestudyidevice')

        # Deleting model 'CaseActivity'
        db.delete_table('exeapp_caseactivity')

        # Deleting model 'Node'
        db.delete_table('exeapp_node')

        # Deleting model 'DublinCore'
        db.delete_table('exeapp_dublincore')

        # Deleting model 'Package'
        db.delete_table('exeapp_package')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exeapp.activityidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ActivityIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Activity'", 'max_length': '100'})
        },
        'exeapp.appletidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'AppletIdevice', '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'java_file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'exeapp.caseactivity': {
            'Meta': {'object_name': 'CaseActivity'},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['exeapp.CaseStudyIdevice']"})
        },
        'exeapp.casestudyidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'CaseStudyIdevice', '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'story': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Case Study'", 'max_length': '100'})
        },
        'exeapp.clozeidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ClozeIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'cloze_text': ('exeapp.models.idevices.fields.ClozeTextField', [], {'default': "''", 'blank': 'True'}),
            'description': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Cloze'", 'max_length': '100'})
        },
        'exeapp.commentidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'CommentIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Remark'", 'max_length': '100'})
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
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ExternalURLIdevice', '_ormbases': ['exeapp.Idevice']},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'exeapp.feedbackidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'FeedbackIdevice', '_ormbases': ['exeapp.Idevice']},
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'exeapp.freetextidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'FreeTextIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'exeapp.genericidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'GenericIdevice', 'db_table': "u'exeapp_idevice'", '_ormbases': ['exeapp.Idevice'], 'proxy': 'True'}
        },
        'exeapp.glossaryidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'GlossaryIdevice', '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Glossary'", 'max_length': '100'})
        },
        'exeapp.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'definition': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idevice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['exeapp.GlossaryIdevice']"}),
            'title': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        'exeapp.idevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Idevice'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'child_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'edit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'idevices'", 'to': "orm['exeapp.Node']"})
        },
        'exeapp.node': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Node'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['exeapp.Package']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['exeapp.Node']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'exeapp.objectivesidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ObjectivesIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Objectives'", 'max_length': '100'})
        },
        'exeapp.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'backgroundImg': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'backgroundImgTile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'dublincore': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.DublinCore']", 'unique': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'footer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'footerImg': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level1': ('django.db.models.fields.CharField', [], {'default': "'Topic'", 'max_length': '20'}),
            'level2': ('django.db.models.fields.CharField', [], {'default': "'Section'", 'max_length': '20'}),
            'level3': ('django.db.models.fields.CharField', [], {'default': "'Unit'", 'max_length': '20'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'resourceDir': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exeapp.pdfidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'PDFIdevice', '_ormbases': ['exeapp.Idevice']},
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'page_list': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'pdf_file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'exeapp.preknowledgeidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'PreknowledgeIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Preknowledge'", 'max_length': '100'})
        },
        'exeapp.readingactivityidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ReadingActivityIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'feedback': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Reading Activity'", 'max_length': '100'}),
            'to_read': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'})
        },
        'exeapp.reflectionidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ReflectionIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'activity': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'answer': ('exeapp.models.idevices.fields.FeedbackField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Reflection'", 'max_length': '100'})
        },
        'exeapp.rssidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'RSSIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'rss_url': ('exeapp.models.idevices.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'RSS'", 'max_length': '100'})
        },
        'exeapp.tocidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'TOCIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'exeapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'exeapp.wikipediaidevice': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'WikipediaIdevice', '_ormbases': ['exeapp.GenericIdevice']},
            'article_name': ('exeapp.models.idevices.fields.URLField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'content': ('exeapp.models.idevices.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'idevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['exeapp.Idevice']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Wiki Article'", 'max_length': '100'})
        }
    }

    complete_apps = ['exeapp']