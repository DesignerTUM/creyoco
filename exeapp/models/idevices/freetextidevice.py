# ===========================================================================
# eXe
# Copyright 2004-2006, University of Auckland
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
FreeTextIdevice: just has a block of text
"""
from django.utils.translation import ugettext_lazy as _
import logging
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices.genericidevice import GenericIdevice
from exeapp.models.idevices import fields

log = logging.getLogger(__name__)

# ===========================================================================

NOEXPORT, PRESENTATION, HANDOUT = "1", "2", "3"

class FreeTextIdevice(GenericIdevice):
    """
    FreeTextIdevice: just has a block of text
    """
    group = Idevice.CONTENT
    name = _("Free Text")
    title = _("Free Text")
    author = _("University of Auckland")
    purpose = _("""The majority of a learning resource will be
establishing context, delivering instructions and providing general information.
This provides the framework within which the learning activities are built and
delivered.""")
    emphasis = Idevice.NOEMPHASIS
    content = fields.RichTextField(blank=True, default="")

    class Meta:
        app_label = "exeapp"


# ===========================================================================

