import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'deployment_settings'

sys.path += ['/home/dimitri/exedjango/src/', '/home/dimitri/exedjango/src/exedjango/'] 

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


