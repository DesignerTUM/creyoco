'''Main view for a user. Handles both GET/POST request and rpc calls'''

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from jsonrpc import jsonrpc_method

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from exeapp.views import upload_file_form
from exeapp.models import Package, User
from exeapp.shortcuts import get_package_by_id_or_error
from exeapp.views.export.exporter_factory import exporter_map


@login_required
def main(request):
    '''Serve the main page with a list of packages.
    TODO: Use a generic view'''
    user = User.objects.get(username=request.user.username)
    package_list = Package.objects.filter(user=user)
    exporter_type_title_map = dict(((export_type, exporter.title) \
                    for export_type, exporter in list(exporter_map.items())))
    form = upload_file_form.UploadFileForm()

    return render_to_response(
        'main.html',
        locals(),
        context_instance=RequestContext(request))

@login_required
def upload_zip(request):
    if upload_file_form.upload_temp_zip(request):
        return HttpResponseRedirect('/')
    else:
        messages.error(request, "Import failed: Wrong type of file")
        return HttpResponseRedirect("/")


@jsonrpc_method('main.create_package', authenticated=True)
def create_package(request, package_name):
    user = User.objects.get(username=request.user.username)
    p = Package.objects.create(title=package_name, user=user)
    return {'id': p.id, 'title': p.title}


@jsonrpc_method('main.delete_package', authenticated=True)
@get_package_by_id_or_error
def delete_package(request, package):
    '''Removes a package'''

    package_id = package.id
    if package.user == request.user:
        package.delete()
        return {"package_id": package_id}
    else:
        return {"package_id": -1}
    package.delete()
    return {"package_id": package_id}


@jsonrpc_method('main.duplicate_package', authenticated=True)
@get_package_by_id_or_error
def duplicate_package(request, package):
    '''Duplicates a package'''
    p = package.duplicate()
    return {"id": p['id'], "title": p['title']}

