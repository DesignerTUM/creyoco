'''Handlers for jsonRPC call from package page outline actions'''

import logging

from jsonrpc import jsonrpc_method
from django.contrib.auth.models import User

from exeapp.shortcuts import get_package_by_id_or_error, \
    jsonrpc_authernticating_method
from exeapp.models.package import Package


log = logging.getLogger()

__all__ = ['add_node', 'delete_node', 'change_current_node',
           'rename_current_node', 'move_current_node_up']


@jsonrpc_authernticating_method('package.add_child_node')
def add_node(request, package, node, new_name=None):
    '''Handles jsonRPC request "package.add_node". Adds a new node
to package_node_id as child of the current one and selectes it'''
    newNode = node.create_child(new_name)
    return {'id': newNode.id, 'title': newNode.title}


@jsonrpc_authernticating_method('package.delete_node')
def delete_node(request, package, node):
    '''Handles jsonRPC request "package.delete_current_node". Removes current
node'''
    new_node_id = node.delete()
    return {'new_node': new_node_id}


@jsonrpc_authernticating_method('package.rename_current_node')
def rename_current_node(request, package, node, new_title):
    '''Handles jsonRPC request "package.rename_current_node". Renames current
node to it's title'''
    node_title = node.rename(new_title)
    return {'title': node_title}


@jsonrpc_authernticating_method('package.duplicate_node')
def duplicate_node(request, package, node):
    '''Duplicate the node and append it to the same root'''
    output = node.duplicate()

    def marshal_output(node):
        children = []
        for child in node['children']:
            children.append(marshal_output(child))
        return {'id': node['node'].id,
                'title': node['node'].title,
                'children': children}

    return marshal_output(output)


@jsonrpc_authernticating_method('package.promote_current_node')
def promote_current_node(request, package, node):
    '''Handles jsonRPC request "package.promote_current_node". Moves current
node one step up in the hierarchie. Returns json variable promoted = 1
if successful'''
    return {"promoted": node.promote()}


@jsonrpc_authernticating_method('package.demote_current_node')
def demote_current_node(request, package, node):
    '''Handles jsonRPC request "package.demote_current_node". Moves current
node one step up in the hierarchie. Returns json variable demoted = 1
if successful'''
    return {"demoted": node.demote()}


@jsonrpc_authernticating_method('package.move_current_node_up')
def move_current_node_up(request, package, node):
    '''Handles jsonRPC request "package.move_current_node_up". Moves the
current node up leaving it on the same level. Returns json variable moved = 1
if successful'''
    return {"moved": node.up()}


@jsonrpc_authernticating_method('package.move_current_node_down')
def move_current_node_down(request, package, node):
    '''Handles jsonRPC request "package.move_current_node_down". Moves the
current node down leaving it on the same level. Returns json variable moved = 1
if successful'''
    return {"moved": node.down()}

@jsonrpc_authernticating_method('package.move_node_before')
def move_node_before(request, package, node, target):
    return node.before(target)


@jsonrpc_authernticating_method('package.move_node_after')
def move_node_after(request, package, node, target):
    return node.after(target)


@jsonrpc_authernticating_method('package.move_node_last')
def move_node_last(request, package, node, target):
    return node.last(target)


@jsonrpc_method('package.create_package', authenticated=True)
def create_package(request, package_name):
    user = User.objects.get(username=request.user.username)
    p = Package.objects.create(title=package_name, user=user)
    return {'id': p.id, 'title': p.title, 'url': p.get_absolute_url()}




@jsonrpc_method('package.delete_package', authenticated=True)
@get_package_by_id_or_error
def delete_package(request, package):
    '''Removes a package'''

    package_id = package.id
    package.delete()
    return {"package_id": package_id}
