# ===========================================================================
# eXe
# Copyright 2004-2005, University of Auckland
# Copyright 2004-2008 eXe Project, http://eXeLearning.org/
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================
"""
WebsiteExport will export a package as a website of HTML pages
"""
from django.core import serializers
from django.conf import settings
import logging
import os
import json
from io import BytesIO
from exeapp.models import Package, Node
from exeapp.utils.path import Path
from exeapp.views.export.websitepage import WebsitePage
from zipfile import ZipFile, ZIP_DEFLATED
import tempfile
from urllib.parse import unquote


def _(value):
    """Place holder for translation"""
    return value


log = logging.getLogger(__name__)


class WebsiteExport(object):
    """
    WebsiteExport will export a package as a website of HTML pages
    """
    title = "Website (Zip)"
    wiki_media = set()
    nonwiki_media = set()

    def __init__(self, package, file_obj):
        """
        'style_dir' is the directory where we can copy the stylesheets from
        'output_dir' is the directory that will be [over]written
        with the website
        """
        static_dir = Path(settings.STATIC_ROOT)
        self.package = package
        self.style_dir = static_dir / "css" / "styles" / package.style
        self.scripts_dir = static_dir / "scripts"
        self.pages = []
        self.json_file = self.create_temp_json_file()
        self.file_obj = file_obj
        self.media_dir = Path(package.user.profile.media_path)
        self.media_root = Path(os.path.abspath(settings.MEDIA_ROOT))
        self.page_class = WebsitePage

        self.output_dir = Path(tempfile.mkdtemp())
        print(self.output_dir)

    def export(self):
        """
        Export web site
        Cleans up the previous packages pages and performs the export
        """
        self.create_pages()
        self.save_pages()

        self.copy_files()
        # Zip up the website package
        self.do_zip()
        # Clean up the temporary dir
        self.output_dir.rmtree()

    def do_zip(self):
        """
        Actually saves the zip data. Called by 'Path.safeSave'
        """
        inner_zip_name = self.package.title + '.zip'
        inner_zip = ZipFile(inner_zip_name, "w")
        self.add_dir_to_zip(inner_zip, Path(self.output_dir))
        inner_zip.close()

        outer_zip = ZipFile(self.file_obj, "w")
        self.add_dir_to_zip(outer_zip, Path(self.output_dir))
        outer_zip.write(inner_zip_name)
        outer_zip.close()

    def add_dir_to_zip(self, zipped, path, rel_path=Path(".")):
        """
            Recursively adds the dir in path + relpath and all its child dirs
            to zipped
        """
        for scormFile in (path / rel_path).files():
            zipped.write(scormFile,
                         rel_path / scormFile.basename(),
                         ZIP_DEFLATED)
        for directory in (path / rel_path).dirs():
            self.add_dir_to_zip(zipped, path, rel_path / directory.basename())

    def copy_style_files(self):
        """Copy style fiels to the export package"""
        style_files = ["%s/../base.css" % self.style_dir,
                       "%s/../popup_bg.gif" % self.style_dir]
        style_files += self.style_dir.files("*.css")
        style_files += self.style_dir.files("*.jpg")
        style_files += self.style_dir.files("*.gif")
        style_files += self.style_dir.files("*.svg")
        style_files += self.style_dir.files("*.png")
        style_files += self.style_dir.files("*.js")
        style_files += self.style_dir.files("*.html")
        self.style_dir.copylist(style_files, self.output_dir)
        if (self.style_dir / "img").exists():
            (self.style_dir / "img").copytree(self.output_dir / "img")
        if (self.style_dir / "js").exists():
            (self.style_dir / "js").copytree(self.output_dir / "js")
        if (self.style_dir / "fonts").exists():
            (self.style_dir / "fonts").copytree(self.output_dir / "fonts")

    def copy_licence(self):
        """Copy licence file"""
        if self.package.license == "GNU Free Documentation License":
            # include a copy of the GNU Free Documentation Licence
            (self.templatesDir / 'fdl.html').copyfile(
                self.output_dir / 'fdl.html')

    def copy_files(self):
        """
        Copy all the files used by the website.
        """
        # Copy the style sheet files to the output dir
        self.copy_style_files()
        self.copy_resources()
        self.scripts_dir.copylist(('libot_drag.js',
                                   'bower_components/jquery/jquery.js'),
                                  self.output_dir)
        self.copy_players()
        self.copy_licence()
        self.copy_json()

    def create_pages(self, additional_kwargs=None):
        additional_kwargs = additional_kwargs or {}
        self.pages.append(self.page_class(self.package.root, 1, exporter=self,
                                          **additional_kwargs))
        self.generate_pages(self.package.root, 1, additional_kwargs)

    def save_pages(self):
        for page in self.pages:
            page.save(self.output_dir)

    def copy_players(self):
        has_flowplayer = False
        has_magnifier = False
        has_xspfplayer = False
        is_break = False

        for page in self.pages:
            if is_break:
                break
            for idevice in page.node.idevices.all():
                resources = idevice.as_child().system_resources
                if has_flowplayer and has_magnifier and has_xspfplayer:
                    is_break = True
                    break
                if not has_flowplayer:
                    if 'flowPlayer.swf' in resources:
                        has_flowplayer = True
                if not has_magnifier:
                    if 'magnifier.swf' in resources:
                        has_magnifier = True
                if not has_xspfplayer:
                    if 'xspf_player.swf' in resources:
                        has_xspfplayer = True

    def copy_resources(self):
        view_media = set()
        for page in self.pages:
            view_media = view_media.union(page.view_media._js). \
                union(page.view_media._css.get('all', []))
        view_media = [unquote(medium.replace(settings.STATIC_URL, ""))
                      for medium in view_media
                      if not "tinymce" in medium]
        Path(settings.STATIC_ROOT).copylist(view_media, self.output_dir)
        for x in self.package.resources:
            if settings.WIKI_CACHE_DIR in x:
                self.wiki_media.add(x)
            else:
                self.nonwiki_media.add(x)
        self.media_dir.copylist(self.nonwiki_media, self.output_dir)
        self.media_root.copylist(self.wiki_media, self.output_dir)

    def generate_pages(self, node, depth, kwargs=None):
        """
        Recursively generate pages and store in pages member variable
for retrieving later. Kwargs will be used at page creation.
        """
        kwargs = kwargs or {}
        for child in node.children.all():
            page = self.page_class(child, depth,
                                   exporter=self,
                                   has_children=child.children.exists(),
                                   **kwargs)

            last_page = self.pages[-1] if self.pages else None
            if last_page:
                page.prev_page = last_page
                last_page.next_page = page
            self.pages.append(page)
            self.generate_pages(child, depth + 1)

    def _cleanup_dict(self, dic):
        return dict([(x, y) for x, y in dic.items() if not x.startswith('_')])


    def dict_of_node(self, node):
        print(node.id)
        node_dict = self._cleanup_dict(node.__dict__)
        child_list = []
        if node.children.count():
            i = 0
            for child in node.children.all():
                i = i + 1
                print(i)
                child_list.append(self.dict_of_node(child))
        node_dict['children'] = child_list
        node_dict['idevices'] = []
        for idevice in node.idevices.all():
            child = idevice.as_child()
            # add todict for every idevice
            clean_dict = child.to_dict()
            node_dict['idevices'].append(clean_dict)
        return node_dict

    def create_json(self):
        print("json")
        dict_for_json = self._cleanup_dict(self.package.to_dict())
        dict_for_json['files'] = []
        for f in self.wiki_media:
            dict_for_json['files'].append(f)
        for f in self.nonwiki_media:
            dict_for_json['files'].append(f)

        for node in self.package.nodes.all():
            dict_for_json['nodes'] = []
            dict_for_json['nodes'].append(self.dict_of_node(node))

        with open(self.json_file, "w") as out:
            out.write(json.dumps(dict_for_json))


    def copy_json(self):
        self.create_json()
        Path.copyfile(self.json_file, Path.joinpath(self.output_dir, Path("a.json")))

    def create_temp_json_file(self):
        f = tempfile.NamedTemporaryFile(mode='w+t', suffix='.json', prefix='', delete=False)
        _filename = f.name
        f.close()
        return _filename
