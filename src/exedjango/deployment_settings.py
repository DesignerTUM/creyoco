# Django settings for exedjango project.

from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

#DATABASES = {
#        'default' : {
#                'ENGINE' : 'django.db.backends.mysql',
#                'NAME' : 'exedjangodb',
#                'USER' : 'root',
#                'PASSWORD' : 'ssl20qwerty',
#                'HOST' : 'localhost',
#                'PORT' : '',
#        }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/dimitri/db/sqlite.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '129.187.81.136']

SENDFILE_BACKEND = 'sendfile.backends.xsendfile'
