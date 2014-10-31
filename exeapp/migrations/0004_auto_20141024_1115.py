# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import exeapp.models.idevices.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0003_auto_20140919_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectedFreeTextIdevice',
            fields=[
                ('idevice_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='exeapp.Idevice', auto_created=True)),
                ('password', models.CharField(blank=True, max_length=20, help_text='Input password to encrypt content', default='')),
                ('content', exeapp.models.idevices.fields.RichTextField(blank=True, default='')),
                ('date_created', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
            options={
            },
            bases=('exeapp.genericidevice',),
        ),
        migrations.CreateModel(
            name='ProtectedFreeTextVersion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', exeapp.models.idevices.fields.RichTextField(blank=True, default='')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2014, 10, 24, 11, 15, 47, 929001))),
                ('idevice', models.ForeignKey(related_name='versions', to='exeapp.ProtectedFreeTextIdevice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='clozeidevice',
            name='cloze_text',
            field=exeapp.models.idevices.fields.ClozeTextField(blank=True, help_text='Enter the text for the cloze activity in to the cloze field\nby either pasting text from another source or by typing text directly into the\nfield.To select words to hide, double click on the word to select it and\nclick on the underscore button in the toolbar.', default=''),
        ),
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 24, 11, 15, 47, 896318)),
        ),
    ]
