# ===========================================================================
# eXe
# Copyright 2004-2005, University of Auckland
# Copyright 2004-2007 eXe Project, New Zealand Tertiary Education Commission
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
from django.template.loader import render_to_string

"""
This class transforms an eXe node into a page on a self-contained website
"""

import logging
from exeapp.views.export.pages import Page

log = logging.getLogger(__name__)

# ===========================================================================
class WebsitePage(Page):
    """
    This class transforms an eXe node into a page on a self-contained website
    """

    def render(self, full_style_url=False):
        """
        Returns an XHTML string rendering this page.
        If full_style_url is set, render website url for
        styles in pages.
        """
        current_page = self
        return render_to_string("exe/export/websitepage.html", locals())
