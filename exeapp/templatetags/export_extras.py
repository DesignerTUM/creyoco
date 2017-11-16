from django import template, forms

from django.template.loader import render_to_string
from django.template.defaultfilters import unordered_list, stringfilter
from django.utils.safestring import mark_safe

from exeapp.utils import common
from exeapp.views.authoring import get_media_list
from exeapp.views.blocks.blockfactory import block_factory

import os
from django.conf import settings

register = template.Library()


@register.simple_tag
def export_idevice(idevice):
    '''Convinience filter, just renders calls render function of a
block'''

    block = block_factory(idevice.as_child())
    return block.renderView()


# @register.inclusion_tag('navigation_bar.html')


@register.simple_tag
def navigation_bar(current_page, full_url):
    """
    Generate the left navigation string for this page
    """
    package = current_page.node.package
    pages = current_page.exporter.pages

    html = ["<ul>"]

    depth = 1
    html.append("<li>")
    for page in pages:
        if depth == page.depth:
            html.append('</li><li>')
        while depth < page.depth:
            html.append("<ul><li>")
            depth += 1
        while depth > page.depth:
            html.append("</li></ul><li>")
            depth -= 1

        html.append(render_to_string("exe/export/navigation_bar_item.html",
                                     {"page": page,
                                      "current_page": current_page,
                                      "package": package,
                                      "full_url": full_url,
                                      }))
    while depth > 0:
        html.append("</li></ul>")
        depth -= 1
    html.append("</ul>")
    return "\n".join(html)


@register.inclusion_tag("exe/export/licence.html")
def render_licence(current_page):
    """
    Returns an XHTML string rendering the license.
    """
    licences = {"GNU Free Documentation License":
                    "http://www.gnu.org/copyleft/fdl.html",
                "Creative Commons Attribution 3.0 License":
                    "http://creativecommons.org/licenses/by/3.0/",
                "Creative Commons Attribution Share Alike 3.0 License":
                    "http://creativecommons.org/licenses/by-sa/3.0/",
                "Creative Commons Attribution No Derivatives 3.0 License":
                    "http://creativecommons.org/licenses/by-nd/3.0/",
                "Creative Commons Attribution Non-commercial 3.0 License":
                    "http://creativecommons.org/licenses/by-nc/3.0/",
                "Creative Commons Attribution Non-commercial Share Alike 3.0 License":
                    "http://creativecommons.org/licenses/by-nc-sa/3.0/",
                "Creative Commons Attribution Non-commercial No Derivatives 3.0 License":
                    "http://creativecommons.org/licenses/by-nc-nd/3.0/",
                "Creative Commons Attribution 2.5 License":
                    "http://creativecommons.org/licenses/by/2.5/",
                "Creative Commons Attribution-ShareAlike 2.5 License":
                    "http://creativecommons.org/licenses/by-sa/2.5/",
                "Creative Commons Attribution-NoDerivs 2.5 License":
                    "http://creativecommons.org/licenses/by-nd/2.5/",
                "Creative Commons Attribution-NonCommercial 2.5 License":
                    "http://creativecommons.org/licenses/by-nc/2.5/",
                "Creative Commons Attribution-NonCommercial-ShareAlike 2.5 License":
                    "http://creativecommons.org/licenses/by-nc-sa/2.5/",
                "Creative Commons Attribution-NonCommercial-NoDerivs 2.5 License":
                    "http://creativecommons.org/licenses/by-nc-nd/2.5/",
                "Developing Nations 2.0":
                    "http://creativecommons.org/licenses/devnations/2.0/"}

    licence = current_page.node.package.license
    licence_url = licences.get(licence)

    return {"licences": licences,
            "licence": licence,
            "licence_url": licence_url,
            }


@register.filter
@stringfilter
def basename(value):
    return os.path.basename(value)


@register.simple_tag
def view_media(page, full_url):
    if full_url:
        return get_media_list(page.node)
    else:
        js = set()
        css = set()
        for idevice in page.node.idevices.all():
            block = block_factory(idevice.as_child())
            for each in block.media._js:
                js.add("<script src='{}'></script>".format(each.split('/')[-1]))
            for each in block.media._css.get('all', []):
                css.add("<link rel='stylesheet' href='{}' />".format(
                    each.split('/')[-1]))
        return "\n".join(css) + "\n" + "\n".join(js)


@register.filter
def process_internal_links(html, package):
    """
    take care of any internal links which are in the form of:
       href="exe-node:Home:Topic:etc#Anchor"
    For this WebSite Export, go ahead and process the link entirely,
    using the fully exported (and unique) file names for each node.
    """
    return common.renderInternalLinkNodeFilenames(package, html)


@register.simple_tag
def render_custom_include(page, filename):
    include_file = os.path.join(page.exporter.style_dir, filename)
    html = ""
    try:
        with open(include_file) as f:
            for line in f.readlines():
                html += line
    except FileNotFoundError:
        pass

    return html
