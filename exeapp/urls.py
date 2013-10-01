from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import RedirectView
from jsonrpc import jsonrpc_site
from jsonrpc.views import browse as json_browse

import exeapp.views.handlers.package_rpc
import exeapp.views.handlers.package_outline_rpc

from exeapp.views import main

urlpatterns = patterns('',
                       (r'^$', main.main),

                       url(r'^json/$', jsonrpc_site.dispatch,
                           name="jsonrpc_mountpoint"),
                       (r'package/$', RedirectView.as_view(url='/exeapp/')),
                       (r'package/(?P<package_id>\d+)/',
                        include('exeapp.package_urls')),
                       (r'pages', include('django.contrib.flatpages.urls')),
                    )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^json/browse/', json_browse,
                                name='jsonrpc_browser'),
    )
