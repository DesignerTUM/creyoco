'''
Created on May 17, 2011

@author: Alendit
'''
import json as simplejson
from django.contrib.auth.decorators import login_required
from exeapp.shortcuts import get_package_by_id_or_error
from exeapp import shortcuts
from django.http import HttpResponse, HttpResponseRedirect, Http404, \
    HttpResponseNotAllowed, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from exeapp.views.blocks.blockfactory import block_factory
from django.core.urlresolvers import reverse
from django import forms
from exeapp.models.package import Package


@login_required
@get_package_by_id_or_error
def authoring(request, package, current_node):
    '''Handles calls to authoring iframe. Renders exe/authoring.html'''

    if "idevice_id" in request.GET:
        try:
            idevice = current_node.idevices.get(
                                pk=(request.GET['idevice_id']))
            if request.GET.get("media", "") == "true":
                json = simplejson.dumps(get_unique_media_list(
                                        idevice.parent_node, idevice))
                return HttpResponse(json, content_type="text/javascript")

            idevice_html = shortcuts.render_idevice(idevice)
            return HttpResponse(idevice_html)
        except ObjectDoesNotExist as e:
            raise Http404(e)
    # if partial is set return only content of body
    elif "media" in request.GET and request.GET['media'] == "true":
        return HttpResponse(get_media_list(current_node, ajax=True),
                             content_type="text/javascript")
    else:
        return HttpResponseBadRequest("No idevice id given.")


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
    media = forms.Media(js=["/static/tiny_mce/tiny_mce.js"])
    js_modules = set()
    for idevice in node.idevices.all():
        idevice = idevice.as_child()
        block = block_factory(idevice)
        media += block.media
        js_modules = js_modules.union(block.js_modules)
    if ajax:
        # don't include tinymce js in ajax script loading
        if "/static/tiny_mce/tiny_mce.js" in media._js:
            media._js.remove("/static/tiny_mce/tiny_mce.js")
        return simplejson.dumps(
            {"js": media._js,
             "css": media._css.get('all', []),
             "js_modules": list(js_modules)
            })
    else:
        return str(media)


def get_unique_media_list(node, idevice):
    '''Returns a list of media which is used only by this idevice'''
    block = block_factory(idevice.as_child())
    media = block.media
    js_modules = block.js_modules
    # compressor is always loaded per default
    if "/static/tiny_mce/tiny_mce.js" in media._js:
        media._js.remove("/static/tiny_mce/tiny_mce.js")
    return {
        'js': media._js,
        'css': media._css,
        'js_modules': js_modules
    }


@login_required
@get_package_by_id_or_error
def link_list(request, package):
    html = "var tinyMCELinkList = %s;" % \
        simplejson.dumps(package.link_list)
    return HttpResponse(html, content_type="application/x-javascript")
