from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest,\
    Http404
from django.core.servers.basehttp import FileWrapper 
from django.core.exceptions import ObjectDoesNotExist

from exeapp.models import Package, User, idevice_store, Package
from exeapp.views.export.websiteexport import WebsiteExport
from exeapp import shortcuts
from exeapp.shortcuts import get_package_by_id_or_error

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
import logging

log = logging.getLogger(__name__)

__all__ = ['package', 'authoring', 'properties']

@login_required
@get_package_by_id_or_error
def package(request, package):
    '''Handle calls to package site. Renders exe/mainpage.html.'''
    
    if package.user.username != request.user.username:
        return HttpResponseForbidden("You don't have an access to this package")
    else:
        data_package = package
        log.info("%s accesses package of %s" % (request.user.username, 
                                                package.user.username))
        idevices = idevice_store.values()
        return render_to_response('exe/mainpage.html', locals())



@login_required
def properties(request, package_id):
    '''Handles calls to properties iframe.'''
    
    return HttpResponse("<h1>Properties for %s</h1>" % package_id)

@login_required
@get_package_by_id_or_error
def export(request, package, format):
    
    if format == "website":
        file_obj = StringIO()
        data_package = package
        exporter = WebsiteExport(data_package, file_obj)
        exporter.exportZip()
        zip = file_obj.getvalue()
        file_obj.close()
        response = HttpResponse(content_type="application/zip")
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=%s.zip'\
                                    % package.title
        response['Content-Length'] = len(zip)
        response.write(zip)
        return response
    else:
        return HttpResponseBadRequest