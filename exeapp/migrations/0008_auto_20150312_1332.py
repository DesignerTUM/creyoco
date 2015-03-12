# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0007_auto_20141107_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 13, 32, 6, 21151)),
        ),
        migrations.AlterField(
            model_name='package',
            name='style',
            field=models.CharField(default='tum2', max_length=20),
        ),
        migrations.AlterField(
            model_name='protectedfreetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 13, 32, 6, 53546)),
        ),
    ]
