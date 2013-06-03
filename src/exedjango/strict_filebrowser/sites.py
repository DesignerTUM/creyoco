"""Custom filebrowser implementation for creyoco"""
from django.core.files.storage import DefaultStorage
from django.http import HttpResponseForbidden, QueryDict
from filebrowser.sites import FileBrowserSite
from filebrowser.settings import *
from filebrowser.actions import *

import os
from functools import wraps


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


class StrictFilebrowserSite(FileBrowserSite):
    """Overrides filebrowser's default directory selection.
    Bases it on the user name"""

    def filebrowser_view(self, view):
        super_view = super(StrictFilebrowserSite, self).filebrowser_view(
            view
        )
        return strict_decorator(view)


storage = DefaultStorage()
storage.location = MEDIA_ROOT
storage.base_url = MEDIA_URL
# Default FileBrowser site
site = StrictFilebrowserSite(name='filebrowser', storage=storage)

# Default actions
site.add_action(flip_horizontal)
site.add_action(flip_vertical)
site.add_action(rotate_90_clockwise)
site.add_action(rotate_90_counterclockwise)
site.add_action(rotate_180)
