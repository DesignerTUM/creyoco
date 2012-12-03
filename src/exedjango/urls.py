from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to

from django.contrib import admin
from django.core.urlresolvers import reverse
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', include('exeapp.urls')),
    (r'grappelli', include('grappelli.urls')),
    (r'filebrowser/', include('filebrowser.urls')),
    (r'tinymce/', include('tinymce.urls')),
    (r'^exeapp/', include('exeapp.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.simple.urls')),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }, name="media-url"),
   )
