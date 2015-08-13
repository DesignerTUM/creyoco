# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import exeapp.models.idevices.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0008_auto_20150312_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='multichoiceoptionidevice',
            name='feedback',
            field=exeapp.models.idevices.fields.RichTextField(help_text='Feedback text for the answer', verbose_name='Feedback', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 11, 23, 50, 8738)),
        ),
        migrations.AlterField(
            model_name='protectedfreetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 11, 23, 50, 31445)),
        ),
    ]
