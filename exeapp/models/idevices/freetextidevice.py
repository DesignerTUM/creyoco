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
from bs4 import BeautifulSoup
from django.utils.translation import ugettext_lazy as _
import logging

from exeapp.utils.path import Path
from datetime import datetime
from django.db import models
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices.genericidevice import GenericIdevice
from exeapp.models.idevices import fields
from django.conf import settings
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
    date_created = models.DateTimeField(blank=True, null=True, editable=False)
    class Meta:
        app_label = "exeapp"

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'id'
                                    and k != 'idevice_ptr_id'
                                    and k != 'parent_node_id'
                                    and k != 'date_created'
                                    and not k.startswith('_')
            }
        d['child_type'] = self.get_klass()
        soup = BeautifulSoup(d['content'])
        images = soup.findAll("img")
        for img in images:
            img['src'] = Path(img['src']).basename()
        d['content'] = soup.prettify()
        return d

    def from_dict(self, dic):
        print(dic)
        self.edit = dic['edit']
        soup = BeautifulSoup(dic['content'])
        images = soup.findAll("img")
        for img in images:
            img['src'] = Path.joinpath(self.parent_node.package.user.profile.media_url, img['src'])
        self.content = soup.prettify()
        self.date_created = datetime.now()
        self.save()
        FreeTextVersion.objects.create(idevice=self, content=self.content, date_created=self.date_created)
        return self

    def has_previous_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return False
        if FreeTextVersion.objects.filter(idevice_id=self.id, date_created__lt=date).count():
            return True
        else:
            return False

    def has_later_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return False
        if FreeTextVersion.objects.filter(idevice_id=self.id, date_created__gt=date).count():
            return True
        else:
            return False

    def get_previous_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return None
        f1 = FreeTextVersion.objects.filter(idevice_id=self.id, date_created__lt=date).order_by('-date_created')
        if f1.count() > 0:
            return f1[0]
        else:
            return None

    def get_later_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return None
        f = FreeTextVersion.objects.filter(idevice_id=self.id, date_created__gt=date).order_by('date_created')
        if f.count() > 0:
            return f[0]
        else:
            return None

    def get_current_version(self):
        f = FreeTextVersion.objects.filter(idevice_id=self.id, date_created=self.date_created)
        if f.count() > 0:
            return f[0]
        else:
            return None

    def delete_unnecessary_version(self):
        FreeTextVersion.objects.filter(idevice_id=self.id, date_created__gt=self.date_created).delete()

    def apply_changes(self, formdata, formsetdata=None):
        #check for first time. it is none at first
        if self.date_created:
            self.delete_unnecessary_version()
        #check for same old version saving again. avoid duplication during creating versions
        v = self.get_current_version()
        if v is None:
            self.date_created = datetime.now()
            FreeTextVersion.objects.create(idevice=self, content=formdata['content'], date_created=self.date_created)
        elif self.content != v.content:
            self.date_created = datetime.now()
            FreeTextVersion.objects.create(idevice=self, content=formdata['content'], date_created=self.date_created)
        self.edit = False


# ===========================================================================

class FreeTextVersion(models.Model):
    idevice = models.ForeignKey("FreeTextIdevice", related_name="versions")
    content = fields.RichTextField(blank=True, default="")
    date_created = models.DateTimeField(default=datetime.now())

    class Meta:
        app_label = "exeapp"

