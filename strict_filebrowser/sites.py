"""Custom filebrowser implementation for creyoco"""
import os
from functools import wraps

from django.core.files.storage import DefaultStorage
from django.http import HttpResponseForbidden
from django.views.decorators.cache import never_cache

from filebrowser.sites import FileBrowserSite
import filebrowser.sites
from django.conf import settings
from filebrowser.actions import *


def strict_decorator(func):
    """Takes a method and inserts user name into the query path"""

    @wraps(func)
    def wrapper(request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden("Please log in")
        username = request.user.username
        target_dir = request.GET.get("dir", '')
        if not target_dir.startswith(username):
            new_query_dict = request.GET.copy()
            new_query_dict['dir'] = os.path.join(username, target_dir)
            request.GET = new_query_dict
        return func(request)

    return wrapper


def filebrowser_view_override(view):
    """ Add a strict decorator """
    return strict_decorator(never_cache(view))

# Monkey patch the view dispatcher
filebrowser.sites.filebrowser_view = filebrowser_view_override


class StrictFilebrowserSite(FileBrowserSite):
    """Is there just so the app works"""
    pass


storage = DefaultStorage()
storage.location = settings.MEDIA_ROOT
storage.base_url = settings.MEDIA_URL
# Default FileBrowser site
site = StrictFilebrowserSite(name='filebrowser', storage=storage)

# Default actions
site.add_action(flip_horizontal)
site.add_action(flip_vertical)
site.add_action(rotate_90_clockwise)
site.add_action(rotate_90_counterclockwise)
site.add_action(rotate_180)
