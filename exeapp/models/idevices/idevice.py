# ===========================================================================
# eXe
# Copyright 2004-2006, University of Auckland
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
import os
from django.conf import settings
from django.db.models.fields import AutoField
import exeapp.models

"""
The base class for all iDevices
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

import logging
# from exe.engine.translate import lateTranslate

log = logging.getLogger(__name__)


# ===========================================================================
class Idevice(models.Model):
    """
    The base model for all iDevices
    iDevices are mini templates which the user uses to create content in the
    package
    """

    # Class attributes
    # see derieved classes for persistenceVersion
    NOEMPHASIS, SOMEEMPHASIS, STRONGEMPHASIS = list(range(3))
    CONTENT, DIDACTICS, COMMUNICATION, TEST, MEDIA, UNKNOWN = \
        _("Content"), _("Didactics"), _("Communication"), _("Test"), \
        _("Media"), _("Unknown")

    GROUP_ORDER = [CONTENT, DIDACTICS, COMMUNICATION, TEST, MEDIA, UNKNOWN]

    # should be overwritten by child classes
    title = ""
    emphasis = NOEMPHASIS
    autor = ""
    purpose = ""
    tip = ""
    system_resources = []

    edit = models.BooleanField(default=True)
    icon = ""
    parent_node = models.ForeignKey('Node', related_name='idevices')

    child_type = models.CharField(max_length=32, editable=False, blank=True)

    def get_klass(self):
        if hasattr(self, 'class_'):
            if self.class_ == '':
                return 'customIdevice'
            else:
                return self.class_ + 'Idevice'
        else:
            klass = str(self.as_child().__class__).split('.')[-1]
            return klass[:-2]

    klass = property(get_klass)

    def icon_url(self):
        icon_url = "%scss/styles/%s/%s" % (settings.STATIC_URL,
                                           self.parent_node.package.style,
                                           self.icon)
        return icon_url

    @property
    def base_idevice(self):
        return Idevice.objects.get(pk=self.pk)

    @property
    def resources(self):
        '''Safe attritube, which checks if idevice owner has the right to
reference the resources'''
        resources = set((resource for resource in self._resources() \
                         if not os.path.normpath(resource). \
            startswith(os.path.pardir)))
        if self.icon:
            resources.add(os.path.join(settings.STATIC_ROOT,
                                       "css/styles/",
                                       self.parent_node.package.style,
                                       self.icon))
        return resources

    def _resources(self):
        '''Should be overridden in children to specify resource
finding. Returns a set'''
        return set()

    @property
    def link_list(self):
        '''Should be overridden in children to specify resource
finding. Returns a list of (name, url) tuples'''
        return []

    def edit_mode(self):
        '''Sets idevice mode to edit'''
        self.edit = True

    def delete(self):
        super(Idevice, self).delete()

    def apply_changes(self, formdata, formsetdata=None):
        self.edit = False


    def is_first(self):
        """
        Return true if this is the first iDevice in this node
        """
        return self._order == 0


    def is_last(self):
        """
        Return true if this is the last iDevice in this node
        """
        return self._order == \
               len(self.parent_node.idevices.get_query_set()) - 1

    def move_up(self):
        """
        Move to the previous position
        """
        # Had to access _order directly because of a strange bug
        # May be reverted to use normal set_idevice_order routine
        # get_previous_in_order doesn't work either.
        base_idevice = self.base_idevice
        prev_idevice = base_idevice.get_previous_in_order()
        prev_idevice._order, self._order = \
            self._order, prev_idevice._order
        prev_idevice.save()
        self.save()

    def move_down(self):
        """
        Move to the next position
        """
        prev_idevice = self.base_idevice.get_next_in_order()
        prev_idevice._order, self._order = self._order, prev_idevice._order
        prev_idevice.save()
        self.save()

    def clone(self):
        initial = {field.name: getattr(self, field.name)
                   for field in self._meta.fields
                   if not isinstance(field, AutoField) and
                   not field in list(self._meta.parents.values())}
        return self.__class__(**initial)

    # Kudos to crucialfelix for djangosnippet 1031
    # http://djangosnippets.org/snippets/1031/
    def save(self, *args, **kwargs):
        if (not self.child_type):
            self.child_type = self.__class__.__name__.lower()
        self.save_base(*args, **kwargs)

    def as_child(self):
        return getattr(self, self.child_type)


    def setParentNode(self, parentNode):
        """
        Change parentNode
        Now includes support for renaming any internal anchors and their link_list.
        """
        old_node = None
        if self.parentNode:
            old_node = self.parentNode
            self.parentNode.idevices.remove(self)
        parentNode.add_idevice(self)
        # and update any internal anchors and their link_list:
        self.ChangedParentNode(old_node, parentNode)


    def getResourcesField(self, this_resource):
        """
        Allow resources to easily find their specific corresponding field,
        to help out with loading and especially merging scenarios for resources
        with names already in use, for example.
        This method is expected to be overridden within each specific iDevice.
        """
        # in the parent iDevice class, merely return a None,
        # and let each specific iDevice class implement its own version:
        log.warn("getResourcesField called on iDevice; no specific "
                 + "implementation available for this particular iDevice "
                 + "class: " + repr(self))
        return None

    def getRichTextFields(self):
        """
        Like getResourcesField(), a general helper to allow nodes to search
        through all of their fields without having to know the specifics of each
        iDevice type.
        Currently used by Extract to find all fields which have internal link_list.
        """
        # in the parent iDevice class, merely return an empty list,
        # and let each specific iDevice class implement its own version:
        log.warn("getRichTextFields called on iDevice; no specific "
                 + "implementation available for this particular iDevice "
                 + "class: " + repr(self))
        return []

    def __unicode__(self):
        return "FreeTextIdevice: %s" % self.id

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'id'
                                    and k != 'idevice_ptr_id'
                                    and k != 'parent_node_id'
                                    and not k.startswith('_')
            }
        d['child_type'] = self.get_klass()
        return d

    def from_dict(self, dic):
        print(dic)
        dic = {k: v for k, v in dic.items() if k != 'child_type'}
        try:
            idevice_class = exeapp.models.idevice_store[self.get_klass()]
        except KeyError:
            raise KeyError("Idevice type %s does not exist." % self.get_klass())
        else:
            idevice_class.objects.filter(id=self.id).update(**dic)
        return self

    @property
    def get_order(self):
        return self._order

    class Meta:
        order_with_respect_to = 'parent_node'
        app_label = "exeapp"
