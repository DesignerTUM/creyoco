# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0006_auto_20141031_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='logoImg',
            field=filebrowser.fields.FileBrowseField(max_length=100, verbose_name='Image', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 7, 14, 14, 34, 170686)),
        ),
        migrations.AlterField(
            model_name='protectedfreetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 7, 14, 14, 34, 204536)),
        ),
    ]
