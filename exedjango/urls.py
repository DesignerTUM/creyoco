from django.conf.urls import *

from django.contrib import admin
from exeapp.utils.filebrowser_monkeypatch import monkey_patch_url
from strict_filebrowser.sites import site
admin.autodiscover()

monkey_patch_url()

urlpatterns = patterns('',
    (r'^$', include('exeapp.urls')),
    (r'filebrowser/', include(site.urls)),
    (r'^exeapp/', include('exeapp.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'^media/', include('check_media.urls'),
     )

)

# from django.conf import settings
# if settings.DEBUG:
#    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#        }, name="media-url"),
#   )
