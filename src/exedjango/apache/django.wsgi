import os
import sys
import site



sys.path += ['/home/dimitri/creyoco/src/exedjango/', '/home/dimitri/creyoco/src/']

site.addsitedir("/home/dimitri/.virtualenvs/creyoco/lib/python2.7/site-packages/")

os.environ['DJANGO_SETTINGS_MODULE'] = 'deployment_settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


