# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clozeidevice',
            name='drag_n_drop',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='freetextversion',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 19, 11, 9, 5, 569305)),
        ),
    ]
