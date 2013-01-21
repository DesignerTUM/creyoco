from django.conf.urls.defaults import patterns
from django.conf import settings

# have to import rpc views manually
# from exeapp.views.package_outline_rpc import *

urlpatterns = patterns('exeapp.views',
   (r'^$', 'package.package_root'),
   (r'^(?P<node_id>\d+)/$', 'package.package_main'),
   (r'(?P<node_id>\d+)/authoring/$', 'authoring.authoring'),
   (r'(?P<node_id>\d+)/handle_action/$', 'authoring.handle_action'),
   (settings.LINK_LIST + '$', 'authoring.link_list'),
   (r'download/(?P<export_format>\w*)/$', 'package.export'),
   (r'(?P<node_id>\d+)/preview/(?P<path>.+)$', 'package.preview_static'),
   (r'(?P<node_id>\d+)/preview/$', 'package.preview'),
)
