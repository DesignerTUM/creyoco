# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import exeapp.models.idevices.fields
import datetime
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseActivity',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('activity', exeapp.models.idevices.fields.RichTextField(default='', help_text='Describe the activity tasks relevant to the case storyprovided. These could be in the form of questions or instructions for activity which may lead the learner to resolving a dilemma presented. ', blank=True)),
                ('feedback', exeapp.models.idevices.fields.FeedbackField(default='', help_text='Provide relevant feedback on the situation', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DublinCore',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128)),
                ('creator', models.CharField(blank=True, max_length=128)),
                ('subject', models.CharField(blank=True, max_length=256)),
                ('description', models.TextField(blank=True)),
                ('publisher', models.CharField(blank=True, max_length=128)),
                ('contributors', models.TextField(blank=True, max_length=256)),
                ('date', models.DateField(default=datetime.date.today)),
                ('type', models.CharField(blank=True, max_length=256)),
                ('format', models.CharField(blank=True, max_length=128)),
                ('identifier', models.CharField(blank=True, max_length=128)),
                ('source', models.CharField(blank=True, max_length=128)),
                ('language', models.CharField(blank=True, max_length=32)),
                ('relation', models.CharField(blank=True, max_length=256)),
                ('coverage', models.CharField(blank=True, max_length=128)),
                ('rights', models.CharField(blank=True, max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FreeTextVersion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2014, 9, 18, 16, 35, 3, 614202))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GlossaryTerm',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', exeapp.models.idevices.fields.RichTextField(default='', help_text='Enter term you want to describe', blank=True, max_length=100)),
                ('definition', exeapp.models.idevices.fields.RichTextField(default='', help_text='Enter definition of the term', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Idevice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('edit', models.BooleanField(default=True)),
                ('child_type', models.CharField(blank=True, max_length=32, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GlossaryIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Glossary', max_length=100)),
            ],
            options={
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='FeedbackIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('email', models.EmailField(default='', blank=True, max_length=50)),
                ('subject', models.CharField(default='', blank=True, max_length=200)),
            ],
            options={
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='ExternalURLIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('url', models.CharField(default='', help_text='Enter the URL you wish to display\nand select the size of the area to display it in.', blank=True, max_length=200)),
                ('height', models.PositiveIntegerField(default=300)),
            ],
            options={
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='CaseStudyIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Case Study', max_length=100)),
                ('story', exeapp.models.idevices.fields.RichTextField(default='', help_text='Create the case story. A good case is one\n        that describes a controversy or sets the scene by describing\n        the characters involved and the situation. It should also allow for\n        some action to be taken in order to gain resolution of the\n        situation.', blank=True)),
            ],
            options={
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='AppletIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('java_file', filebrowser.fields.FileBrowseField(verbose_name='Java Applet', blank=True, null=True, max_length=100)),
            ],
            options={
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='MultiChoiceIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Multiple Choice', max_length=100)),
                ('question', exeapp.models.idevices.fields.RichTextField(default='', help_text='Create a multiple choice questionary to review the\n    learned material. Click "Add option" to add more answer options', blank=True)),
            ],
            options={
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='MultiChoiceOptionIdevice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('option', exeapp.models.idevices.fields.MultiChoiceOptionField(default='', help_text="An answer option for the multiple choice question. Check the 'right answer' checkmark to mark the right option", blank=True)),
                ('right_answer', models.BooleanField(default=False)),
                ('idevice', models.ForeignKey(to='exeapp.MultiChoiceIdevice', related_name='options')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('is_root', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=256)),
                ('backgroundImg', models.ImageField(upload_to='background', blank=True, null=True)),
                ('backgroundImgTile', models.BooleanField(default=False)),
                ('footer', models.CharField(blank=True, max_length=100)),
                ('footerImg', models.ImageField(upload_to='footer', blank=True, null=True)),
                ('license', models.CharField(blank=True, max_length=50)),
                ('style', models.CharField(default='default', max_length=20)),
                ('resourceDir', models.FileField(upload_to='resources', blank=True, null=True)),
                ('level1', models.CharField(default='Topic', max_length=20)),
                ('level2', models.CharField(default='Section', max_length=20)),
                ('level3', models.CharField(default='Unit', max_length=20)),
                ('collaborators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='shared_packages')),
                ('dublincore', models.OneToOneField(to='exeapp.DublinCore')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PDFIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('pdf_file', filebrowser.fields.FileBrowseField(verbose_name='PDF', blank=True, null=True, max_length=100)),
                ('modified_pdf_file', models.FilePathField(blank=True, null=True, editable=False)),
                ('page_list', models.CharField(default='', help_text='Input coma-separated pages or page ranges to import. For example: 1,2,3-8. Leave empty to import all pages', blank=True, max_length=50)),
            ],
            options={
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='node',
            name='package',
            field=models.ForeignKey(to='exeapp.Package', related_name='nodes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='exeapp.Node', null=True),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='node',
            order_with_respect_to='parent',
        ),
        migrations.AddField(
            model_name='idevice',
            name='parent_node',
            field=models.ForeignKey(to='exeapp.Node', related_name='idevices'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='idevice',
            order_with_respect_to='parent_node',
        ),
        migrations.AddField(
            model_name='glossaryterm',
            name='idevice',
            field=models.ForeignKey(to='exeapp.GlossaryIdevice', related_name='terms'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='caseactivity',
            name='idevice',
            field=models.ForeignKey(to='exeapp.CaseStudyIdevice', related_name='terms'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='GenericIdevice',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('exeapp.idevice',),
        ),
        migrations.CreateModel(
            name='WikipediaIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Wiki Article', max_length=100)),
                ('article_name', exeapp.models.idevices.fields.URLField(default='', help_text='Enter a phrase or term you\n                                   wish to search\nwithin Wikipedia.', blank=True, max_length=100)),
                ('language', models.CharField(default='en', max_length=2, choices=[('de', 'DE'), ('en', 'EN')])),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='TOCIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='RSSIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='RSS', max_length=100)),
                ('rss_url', exeapp.models.idevices.fields.URLField(default='', help_text='Enter an RSS URL for the RSS\n                              feed you\nwant to attach to your content. Feeds are often identified by a small graphic\n icon (often like this <img src="/static/images/feed-icon.png" />) or the\n text "RSS". Clicking on the\n icon or text label will display an RSS feed right in your browser. You can\n copy and paste the\nURL into this field. Alternately, right clicking on the link or graphic will\nopen a menu box;\nclick on COPY LINK LOCATION or Copy Shortcut. Back in eXe open the RSS\nbookmark iDevice and Paste the URL\ninto the RSS URL field and click the LOAD button. This will extract the\ntitles from your feed and\ndisplay them as links in your content. From here you can edit the bookmarks\nand add\n instructions or additional learning information.', blank=True, max_length=200)),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='ReflectionIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Reflection', max_length=100)),
                ('activity', exeapp.models.idevices.fields.RichTextField(default='', help_text='Enter a question for learners to\n                                        reflect upon.', blank=True)),
                ('answer', exeapp.models.idevices.fields.FeedbackField(default='', help_text='Describe how learners will assess how\nthey have done in the exercise. (Rubrics are useful devices for providing\nreflective feedback.)', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='ReadingActivityIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Reading Activity', max_length=100)),
                ('to_read', exeapp.models.idevices.fields.RichTextField(default='', help_text='Enter the details of the reading\n    including reference details. The\n    referencing style used will depend on the preference of your faculty or\n    department.', blank=True)),
                ('activity', exeapp.models.idevices.fields.RichTextField(default='', help_text='Describe the tasks related to the reading learners should undertake.\n        This helps demonstrate relevance for learners.', blank=True)),
                ('feedback', exeapp.models.idevices.fields.FeedbackField(default='', help_text='Use feedback to provide a summary of the points covered in the reading,\nor as a starting point for further analysis of the reading by posing a question\nor providing a statement to begin a debate.', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='PreknowledgeIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Preknowledge', max_length=100)),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', help_text='Describe the prerequisite knowledge learners\n                        should have to effectively complete this learning.', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='ObjectivesIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Objectives', max_length=100)),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', help_text='Type the learning objectives for this resource.', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='FreeTextIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', blank=True)),
                ('date_created', models.DateTimeField(blank=True, null=True, editable=False)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.AddField(
            model_name='freetextversion',
            name='idevice',
            field=models.ForeignKey(to='exeapp.FreeTextIdevice', related_name='versions'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CommentIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Remark', max_length=100)),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', help_text="Use this field to leave a\ncomment for people who works on this package with you.\nThis iDevice won't be exported", blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='ClozeIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Cloze', max_length=100)),
                ('description', exeapp.models.idevices.fields.RichTextField(default='', help_text='Provide instruction on how the cloze activity should be\ncompleted. Default text will be entered if there are no changes to this field.\n', blank=True)),
                ('cloze_text', exeapp.models.idevices.fields.ClozeTextField(default='', help_text='Enter the text for the cloze activity in to the cloze field\nby either pasting text from another source or by typing text directly into the\nfield.To select words to hide, double click on the word to select it and\nclick on the underscore button in the toolbar.', blank=True)),
                ('feedback', exeapp.models.idevices.fields.FeedbackField(default='', help_text='Enter any feedback you wish to provide the learner\n                with-in the feedback field. This field can be left blank.', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='ActivityIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='exeapp.Idevice')),
                ('title', models.CharField(default='Activity', max_length=100)),
                ('content', exeapp.models.idevices.fields.RichTextField(default='', help_text='Describe the tasks the learners should complete.', blank=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
    ]
