# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0005_auto_20141028_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 31, 16, 18, 30, 178551)),
        ),
        migrations.AlterField(
            model_name='protectedfreetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 31, 16, 18, 30, 211381)),
        ),
    ]
