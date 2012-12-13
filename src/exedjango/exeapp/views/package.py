from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest, \
    Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.core.servers.basehttp import FileWrapper
from django.core.exceptions import ObjectDoesNotExist

from exeapp.models import Package, User, idevice_store, Package
from exeapp.views.export.websiteexport import WebsiteExport
from exeapp import shortcuts
from exeapp.shortcuts import get_package_by_id_or_error
from django import forms
from django.core.urlresolvers import reverse
from exeapp.models.package import DublinCore
from exeapp.views.export.imsexport import IMSExport
from exeapp.views.export.exporter_factory import exporter_factory, exporter_map

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import logging

log = logging.getLogger(__name__)

__all__ = ['package', 'authoring', 'properties']


class PackagePropertiesForm(forms.ModelForm):
    form_type = "properties_form"
    form_type_field = forms.CharField(initial=form_type,
                                  widget=forms.HiddenInput())

    class Meta:
        model = Package
        fields = ('title', 'author', 'email', 'description')

class DublinCoreForm(forms.ModelForm):
    form_type = "dublincore_form"
    form_type_field = forms.CharField(initial=form_type,
                                  widget=forms.HiddenInput())

    class Meta:
        model = DublinCore


def generate_package_main(request, package, **kwargs):
    '''Generates main page, can take additional keyword args to
    create forms'''

    log.info("%s accesses package of %s" % (request.user.username,
                                            package.user.username))
    idevices = idevice_store.values()
    exporter_type_title_map = dict(((export_type, exporter.title) \
                        for export_type, exporter in exporter_map.items()))
    properties_form = kwargs.get(PackagePropertiesForm.form_type,
                                 PackagePropertiesForm(instance=package))
    dublincore_form = kwargs.get(DublinCoreForm.form_type,
                                 DublinCoreForm(instance=package.dublincore))
    user = User.objects.get(username=request.user.username)
    package_list = Package.objects.filter(user=user)
    return render_to_response('exe/mainpage.html', locals())

def change_properties(request, package):
    '''Parses post requests and applies changes to the package'''
    form_type = request.POST['form_type_field']
    if form_type == PackagePropertiesForm.form_type:
        form = PackagePropertiesForm(request.POST, instance=package)
    elif form_type == DublinCoreForm.form_type:
        form = DublinCoreForm(request.POST, instance=package.dublincore)
    if form.is_valid():
        form.save()
        if request.is_ajax():
            return HttpResponse("")
        else:
            return HttpResponseRedirect(reverse('exeapp.views.package.package_main',
                                             args=[package.id]))
    else:
        if request.is_ajax():
            return HttpResponse(form.as_table())
        else:
            return generate_package_main(request, package,
                                         **{form.form_type : form})

@login_required
@get_package_by_id_or_error
def package_main(request, package, properties_form=None):
    '''Handle calls to package site. Renders exe/mainpage.html.'''
    if request.method == 'POST':
        return change_properties(request, package)
    else:
        return generate_package_main(request, package)


@login_required
@get_package_by_id_or_error
def export(request, package, export_format):

    file_obj = StringIO()
    try:
        exporter = exporter_factory(export_format, package, file_obj)
    except KeyError:
        return HttpResponseBadRequest("Invalid export type")
    exporter.export()
    zip_file = file_obj.getvalue()
    file_obj.close()
    response = HttpResponse(content_type="application/zip_file")
    response['Content-Disposition'] = 'attachment; filename=%s.zip_file'\
                                % package.title
    response['Content-Length'] = len(zip_file)
    response.write(zip_file)
    return response


@login_required
@get_package_by_id_or_error
def preview(request, package, node_id):
    exporter = exporter_factory("website", package, None)
    exporter.create_pages()
    print exporter.pages
    print node_id
    for page in exporter.pages:
        print page.node.id
        if page.node.id == int(node_id):
            found_page = page
            break
    return HttpResponse(found_page.render(full_style_url=True))
