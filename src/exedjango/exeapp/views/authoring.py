'''
Created on May 17, 2011

@author: Alendit
'''
from django.contrib.auth.decorators import login_required
from exeapp.shortcuts import get_package_by_id_or_error
from exeapp import shortcuts
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from exeapp.views.blocks.blockfactory import block_factory
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django import forms
from exeapp.models.package import Package


@login_required
@get_package_by_id_or_error
def authoring(request, package, current_node, partial=False):
    '''Handles calls to authoring iframe. Renders exe/authoring.html'''

    if "idevice_id" in request.GET:
        try:
            idevice = package.get_idevice_for_partial\
                        (request.GET['idevice_id'])
            if request.GET.get("media", "") == "true":
                json = simplejson.dumps(get_unique_media_list(
                                        idevice.parent_node, idevice))
                return HttpResponse(json, content_type="text/javascript")

            idevice_html = shortcuts.render_idevice(idevice)
            return HttpResponse(idevice_html)
        except ObjectDoesNotExist, e:
            raise Http404(e)
    # if partial is set return only content of body
    partial = partial or \
                "_pjax" in request.GET
    if partial and "media" in request.GET and request.GET['media'] == "true":
        return HttpResponse(get_media_list(current_node, ajax=True),
                             content_type="text/javascript")
    return render_to_response('exe/authoring.html', locals())


@login_required
@get_package_by_id_or_error
def handle_action(request, package, node):
    '''Handles post action sent from authoring'''
    if request.method == "POST":
        post_dict = dict(request.POST)
        idevice_id = post_dict.pop('idevice_id')[0]
        action = post_dict.pop('idevice_action')[0]
        response = node.handle_action(idevice_id,
                                          action, request.POST)
        return HttpResponse(response)
    return HttpResponse()


def get_media_list(node, ajax=False):
    '''Returns the idevice-specific media list for a given node. Always
includes tinymce compressor, since it can't be loaded dynamically'''
    # always load tinymce compressor
#    media = forms.Media(js=[reverse('tinymce-compressor')])
    media = forms.Media(js=["/static/tiny_mce/tiny_mce.js"])
#    media = forms.Media()
    for idevice in node.idevices.all():
        idevice = idevice.as_child()
        block = block_factory(idevice)
        media += block.media
        # print "#" * 10
        # print media._js
    if ajax:
        # don't include tinymce js in ajax script loading
        if "/static/tiny_mce/tiny_mce.js" in media._js:
            media._js.remove("/static/tiny_mce/tiny_mce.js")
        return simplejson.dumps(media._js + media._css.get('all', []))
    else:
        return str(media)


def get_unique_media_list(node, idevice=None):
    '''Returns a list of media which is used only by this idevice'''
    block = block_factory(idevice.as_child())
    media = block.media._js + block.media._css.get('all', [])
    # compressor is always loaded per default
    if "/static/tiny_mce/tiny_mce.js" in media:
        media.remove("/static/tiny_mce/tiny_mce.js")
    for idevice in node.idevices.exclude(id=idevice.id):
        block = block_factory(idevice.as_child())
        for js in block.media._js + block.media._css.get('all', []):
            if js in media:
                media.remove(js)
    return media


@login_required
@get_package_by_id_or_error
def link_list(request, package):
    html = "var tinyMCELinkList = %s;" % \
        simplejson.dumps(package.link_list)
    return HttpResponse(html, content_type="application/x-javascript")
