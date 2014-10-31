# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0004_auto_20141024_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 20, 10, 59, 640921)),
        ),
        migrations.AlterField(
            model_name='protectedfreetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 20, 10, 59, 671017)),
        ),
    ]
