import os
import sys
import site



sys.path += ['/home/dimitri/exedjango/src/', '/home/dimitri/exedjango/src/exedjango/'] 

site.addsitedir("/home/dimitri/creyoco/django.wsgi")

os.environ['DJANGO_SETTINGS_MODULE'] = 'deployment_settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


