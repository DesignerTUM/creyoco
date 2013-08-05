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
from exeapp.models.idevices.idevice import Idevice
"""
WebsiteExport will export a package as a website of HTML pages
"""

from django.conf import settings

import logging
from exeapp.utils.path import Path
from exeapp.views.export.websitepage import WebsitePage
from zipfile import ZipFile, ZIP_DEFLATED
import tempfile


def _(value):
    """Place holder for translation"""
    return value


log = logging.getLogger(__name__)


class WebsiteExport(object):
    """
    WebsiteExport will export a package as a website of HTML pages
    """
    title = "Website (Zip)"

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
        self.file_obj = file_obj
        self.media_dir = Path(package.user.get_profile().media_path)
        self.page_class = WebsitePage

        self.output_dir = Path(tempfile.mkdtemp())
        print((self.output_dir))

    def export(self):
        """
        Export web site
        Cleans up the previous packages pages and performs the export
        """
        self.create_pages()
        self.save_pages()

        self.copy_files()
        # Zip up the website package
        self.doZip()
        # Clean up the temporary dir
        self.output_dir.rmtree()

    def doZip(self):
        """
        Actually saves the zip data. Called by 'Path.safeSave'
        """
        zipped = ZipFile(self.file_obj, "w")
        for scormFile in self.output_dir.files():
            zipped.write(scormFile, scormFile.basename(), ZIP_DEFLATED)
        zipped.close()

    def copy_style_files(self):
        """Copy style fiels to the export package"""
        style_files = ["%s/../base.css" % self.style_dir]
        style_files.append("%s/../popup_bg.gif" % self.style_dir)
        style_files += self.style_dir.files("*.css")
        style_files += self.style_dir.files("*.jpg")
        style_files += self.style_dir.files("*.gif")
        style_files += self.style_dir.files("*.svg")
        style_files += self.style_dir.files("*.png")
        style_files += self.style_dir.files("*.js")
        style_files += self.style_dir.files("*.html")
        self.style_dir.copylist(style_files, self.output_dir)

    def copy_licence(self):
        """Copy licence file"""
        if self.package.license == "GNU Free Documentation License":
            # include a copy of the GNU Free Documentation Licence
            (self.templatesDir / 'fdl.html').copyfile(\
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

    def create_pages(self, additional_kwargs={}):
        self.pages.append(self.page_class(self.package.root, 1, exporter=self,
                                          **additional_kwargs))
        self.generate_pages(self.package.root, 2, additional_kwargs)

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
                if (has_flowplayer and has_magnifier and has_xspfplayer):
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
        view_media = []
        for page in self.pages:
            view_media += page.view_media._js
            view_media += page.view_media._css.get('all', [])
        view_media = [medium.replace(settings.STATIC_URL, "") \
                      for medium in view_media]
        Path(settings.STATIC_ROOT).copylist(view_media, self.output_dir)
        self.media_dir.copylist(self.package.resources, self.output_dir)

    def generate_pages(self, node, depth, kwargs={}):
        """
        Recursively generate pages and store in pages member variable
for retrieving later. Kwargs will be used at page creation.
        """
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



