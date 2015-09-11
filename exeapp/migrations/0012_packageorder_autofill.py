# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exeapp', '0011_packageorder'),
    ]

    operations = [
        migrations.RunSQL(
            "insert into exeapp_packageorder (package_id, user_id, sort_order) "
            "select id as package_id, user_id, id as sort_order from exeapp_package"
        ),
        migrations.RunSQL(
            "insert into exeapp_packageorder (package_id, user_id, sort_order)"
            "select package_id, user_id, package_id as sort_order from exeapp_package_collaborators"
        )
    ]
