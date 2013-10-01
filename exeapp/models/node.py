# ===========================================================================
# eXe
# Copyright 2004-2006, University of Auckland
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
import re

from django.core.urlresolvers import reverse

"""
Nodes provide the structure to the package hierarchy
"""

from django.db import models

from exeapp.models import idevice_store

import logging
from copy import deepcopy

log = logging.getLogger()


class NodeManager(models.Manager):
    def create(self, package, parent, title=None, is_root=False):
        if title is None:
            level = parent.level + 1
            if level > 3:
                title = "???"
            else:
                title = getattr(package, "level%s" % level)
        node = Node(package=package, parent=parent, title=title,
                    is_root=is_root)
        node.save()
        return node


class Node(models.Model):
    """
    Nodes provide the structure to the package hierarchy
    """
    package = models.ForeignKey('Package', related_name='nodes')
    parent = models.ForeignKey('self', related_name='children',
                               blank=True, null=True)
    title = models.CharField(max_length=50)
    is_root = models.BooleanField(default=False)

    objects = NodeManager()

    # self.last_full_node_path = self.GetFullNodePath()

    # Properties

    # level
    def getLevel(self):
        """
        Calculates and returns our current level
        """
        return len(list(self.ancestors()))

    level = property(getLevel)

    def get_idevice(self, idevice_id):
        '''Returns idevice with given id. Can't use dictionary, because
it is unordered and can't use OrderedDict, because jelly doesn't play nice
with it'''
        for idevice in self.idevices:
            if idevice.id == idevice_id:
                return idevice
        raise KeyError("Idevice %s not found" % idevice_id)

        #

    def GetFullNodePath(self, new_node_title=""):
        """
        A general purpose single-line node-naming convention,
        currently only used for the anchor names, to
        provide a path to its specific node.
        Create this path in an HTML-safe name, to closely match
        the names used upon export of the corresponding files.
        Optional new_node_title allows the determination of the
        full path name should this node's name change.
        """
        # use lower-case for the exe-node, for TinyMCE copy/paste compatibility:
        full_path = "exe-node"
        # first go through all of the parentNode's ancestor nodes:
        this_nodes_ancestors = list(self.ancestors())
        num_ancestors = len(this_nodes_ancestors)
        for loop in range(num_ancestors - 1, -1, -1):
            node = this_nodes_ancestors[loop]
            if node is not None:
                # note: if node is None,
                #   appears to be an invalid ancestor in an Extracted package,
                #   but continue on, since it was probably one of the top nodes
                #   above the extraction that is None.
                # but this node IS valid, so add it to the path:
                full_path = "%s:%s" % (full_path, self.title)

        # and finally, add this node itself:
        if new_node_title == "":
            full_path = "%s:%s" % (full_path, self.title)
        else:
            # a new_node_title was specified, create this path with the new name
            full_path = "%s:%s" % (full_path, new_node_title)
        return full_path

    titleShort = property(lambda self: self.title.split('--', 1)[0].strip())
    titleLong = property(lambda self: self.title.split('--', 1)[-1].strip())

    # Normal methods

    def copyToPackage(self, newPackage, newParentNode=None):
        """
        Clone a node just like this one, still belonging to this package.
        if 'newParentNode' is None, the newly created node will replace the
            root of 'newPackage'

        The newly inserted node is automatically selected.
        """
        log.debug("clone " + self.title)

        try:
            # Setting self.parent in the copy to None, so it doesn't
            # go up copying the whole tree
            newNode = deepcopy(self, {id(self._package): newPackage,
                                      id(self.parent): None})
            newNode._id = newPackage._regNewNode(newNode)
        except Exception as e:
            raise

        # return nonpersistables to normal status:
        # Give all the new nodes id's
        for node in newNode.walkDescendants():
            node._id = newPackage._regNewNode(node)
            # Insert into the new package
        if newParentNode is None:
            newNode.parent = None
            newPackage.root = newPackage.currentNode = newNode
        else:
            newNode.parent = newParentNode
            newNode.parent.children.append(newNode)
            newPackage.currentNode = newNode
        return newNode

    def ancestors(self):
        """Iterates over our ancestors"""
        if self.parent:  # All top level nodes have no ancestors
            node = self
            while node is not None and node is not self.package.root:
                if not hasattr(node, 'parent'):
                    log.warn("ancestor node has no parent")
                    node = None
                else:
                    node = node.parent
                    yield node

    def isAncestorOf(self, node):
        """If we are an ancestor of 'node' returns 'true'"""
        return self in node.ancestors()

    @property
    def resources(self):
        """
        Return the resource files used by this node
        """
        log.debug("getResources ")
        resources = set()
        #        from IPython import embed; embed()
        for idevice in self.idevices.all():
            resources.update(idevice.as_child().resources)

        return resources

    @property
    def link_list(self):
        '''
        Returns all links from idevices and a link to the node itself
        '''
        link_list = [(self.title, "%s.html" % self.unique_name())]
        for idevice in self.idevices.all():
            link_list += idevice.as_child().link_list
        return link_list

    def handle_action(self, idevice_id, action, data):
        '''Removes an iDevice or delegates action to it'''
        idevice = self.idevices.get(pk=idevice_id).as_child()
        from exeapp.views.blocks.blockfactory import block_factory

        block = block_factory(idevice)
        if action == 'delete':
            idevice.delete()
            return ""
        else:
            response = block.process(action, data)
            block.idevice.save()
            return response

    def rename(self, new_title):
        if new_title not in ['', 'null', 'undefined']:
            self.title = new_title
            self.save()
        return self.title

    def create_child(self, new_name=None):
        """
        Create a child node
        """
        log.debug("create_child ")
        return Node.objects.create(package=self.package,
                                   title=new_name,
                                   parent=self)

    def duplicate(self, parent=None):
        """Create a copy of this node"""
        log.debug("Duplicate node {}".format(self.pk))
        children = list(self.children.all())
        idevices = list(self.idevices.all())
        node = self
        if parent is not None:
            node.parent = parent
        elif node.parent is None and node.is_root:
            node.is_root = False
            node.parent = self
        node.pk = None
        node.save()
        for idevice in idevices:
            new_idevice = idevice.as_child().clone()
            new_idevice.parent_node = node
            new_idevice.save()
        children_return = []
        for child in children:
            children_return.append(child.duplicate(parent=node))
        return {'node': node, "children": children_return}

    def add_idevice(self, idevice_type):
        """
        Add the idevice to this node, sets idevice's parentNode. Throws
        KeyError, if idevice_type is not found
        """
        log.debug("add_idevice %s" % idevice_type)
        try:
            idevice_class = idevice_store[idevice_type]
        except KeyError:
            raise KeyError("Idevice type %s does not exist." % idevice_type)
        else:
            for edited_device in self.idevices.filter(edit=True):
                edited_device.edit = False
                edited_device.save()
            idevice = idevice_class.objects.create(parent_node=self)
            return idevice

    def move(self, new_parent, next_sibling=None):
        """
        Moves the node around in the tree.
        """

        self.parent = new_parent
        self.save()
        node_order = self.parent.get_node_order()
        node_order.remove(self.id)
        if next_sibling is not None:
            sibling_index = node_order.index(next_sibling.pk)
        else:
            sibling_index = len(node_order)
        node_order.insert(sibling_index, self.pk)
        self.parent.set_node_order(node_order)

    def promote(self):
        """
        Convenience function. Moves the node one step
closer to the tree root.
Returns True is successful
        """
        log.debug("promote ")
        if self.parent and self.parent.parent:
            try:
                next_sibling = self.parent.get_next_in_order()
            except Node.DoesNotExist:
                next_sibling = None
            self.move(self.parent.parent, next_sibling)
            return True

        return False

    def demote(self):
        """
        Convenience function. Moves the node one step further away
from its parent, tries to keep the same position in the tree.
Returns True is successful
        """
        log.debug("demote ")
        if self.parent:
            try:
                new_parent = self.get_previous_in_order()
            except Node.DoesNotExist:
                return False
            if new_parent is not None:
                self.move(new_parent)
                return True

        return False

    def up(self):
        """
        Moves the node up one node vertically, keeping to the same level in
        the tree.
        Returns True is successful.
        """
        log.debug("up ")
        try:
            prev_sibling = self.get_previous_in_order()
        except Node.DoesNotExist:
            return False
        if prev_sibling is not None:
            self.move(self.parent, prev_sibling)
            return True
        return False

    def down(self):
        """
        Moves the node down one vertically, keeping its level the same.
        Returns True is successful.
        """
        log.debug("down ")
        try:
            next_sibling = self.get_next_in_order()
        except Node.DoesNotExist:
            return False
        try:
            next_next_sibling = next_sibling.get_next_in_order()

        except Node.DoesNotExist:
            next_next_sibling = None

        self.move(self.parent, next_next_sibling)
        return True

    def delete(self):
        """Checks if the node is root, deletes it otherwise.
        Returns parents id"""
        if self.is_root:
            return 0
        else:
            parent_id = self.parent.id
            super(Node, self).delete()
            return parent_id

    def walkDescendants(self):
        """
        Generator that walks all descendant nodes
        """
        for child in self.children.all():
            yield child
            for descendant in child.walkDescendants():
                yield descendant


    def unique_name(self):
        '''Returns the name for saving'''
        if self.is_root:
            return "index"
        else:
            page_name = self.title.lower().replace(" ", "_")
            page_name = re.sub(r"\W", "", page_name)
            if not page_name:
                page_name = "__"
            page_name = "%s_%s" % (page_name, self.id)
            return page_name

    def url(self):
        return reverse("exeapp.views.package.package_main",
                       args=[self.package.id, self.id])

    def __unicode__(self):
        """
        Return a node as a string
        """

        return "Node %s" % self.title

    class Meta:
        app_label = "exeapp"
        order_with_respect_to = 'parent'

# ===========================================================================
