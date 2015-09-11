# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0009_auto_20150807_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='protectedfreetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
