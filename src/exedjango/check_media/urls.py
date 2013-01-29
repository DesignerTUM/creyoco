'''
Created on Jan 29, 2013

@author: alendit
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                      (r'(?P<path>.+)$', "check_media.views.serve_media"),
                      )
