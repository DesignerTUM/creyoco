# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import exeapp.models.idevices.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0002_auto_20140919_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clozeidevice',
            name='cloze_text',
            field=exeapp.models.idevices.fields.RichTextField(blank=True, default='', help_text='Enter the text for the cloze activity in to the cloze field\nby either pasting text from another source or by typing text directly into the\nfield.To select words to hide, double click on the word to select it and\nclick on the underscore button in the toolbar.'),
        ),
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 19, 15, 47, 37, 133556)),
        ),
    ]
