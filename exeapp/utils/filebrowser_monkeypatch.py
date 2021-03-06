import types
from django.views.decorators.cache import never_cache
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from filebrowser.decorators import path_exists, file_exists
from strict_filebrowser.sites import site, filebrowser_view_override

def get_urls(self):
    "URLs for a filebrowser.site"
    try:
        from django.conf.urls import url, patterns
    except ImportError:
        # for Django version less then 1.4
        from django.conf.urls.defaults import url, patterns

    # filebrowser urls (views)
    urlpatterns = patterns(
        '',
        url(r'^browse/$', path_exists(self, filebrowser_view_override(self.browse)), name="fb_browse"),
        url(r'^createdir/', path_exists(self, filebrowser_view_override(self.createdir)), name="fb_createdir"),
        url(r'^upload/', path_exists(self, filebrowser_view_override(self.upload)), name="fb_upload"),
        url(r'^delete_confirm/$', file_exists(self, path_exists(self, filebrowser_view_override(self.delete_confirm))), name="fb_delete_confirm"),
        url(r'^delete/$', file_exists(self, path_exists(self, filebrowser_view_override(self.delete))), name="fb_delete"),
        url(r'^detail/$', file_exists(self, path_exists(self, filebrowser_view_override(self.detail))), name="fb_detail"),
        url(r'^version/$', file_exists(self, path_exists(self, filebrowser_view_override(self.version))), name="fb_version"),
        url(r'^upload_file/$', csrf_exempt(self._upload_file), name="fb_do_upload"),
    )
    return urlpatterns



def monkey_patch_url():
    site.get_urls = types.MethodType(get_urls, site)
