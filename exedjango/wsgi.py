import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exedjango.deployment_settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exedjango.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
