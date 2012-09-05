import os
import sys
import site



sys.path += ['/home/dimitri/creyoco/src/exedjango/', '/home/dimitri/creyoco/src/'] 

site.addsitedir("/home/dimitri/creyoco_env/lib/python2.7/site-packages/")

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


