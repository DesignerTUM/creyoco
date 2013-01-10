from django.conf.urls.defaults import *
from django.conf import settings

# have to import rpc views manually
# from exeapp.views.package_outline_rpc import *

urlpatterns = patterns('exeapp.views',
   (r'^$', 'package.package_root'),
   (r'^/(?P<node_id>\d+/$', 'package.package_main'),
   (r'authoring/$', 'authoring.authoring'),
   (r'handle_action/$', 'authoring.handle_action'),
   (settings.LINK_LIST + '$', 'authoring.link_list'),
   (r'authoring/(?P<page_name>\w*).html$', 'authoring.change_page'),
   (r'download/(?P<format>\w*)/$', 'package.export'),
   (r'preview/(?P<node_id>\d+)/(?P<path>.+)$', 'package.preview_static'),
   (r'preview/(?P<node_id>\d+)/$', 'package.preview'),
)
