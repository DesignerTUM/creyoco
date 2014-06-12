from functools import wraps

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from jsonrpc import jsonrpc_method
from exeapp.models import Package
from exedjango.base.http import Http403
from exeapp.views.blocks.blockfactory import block_factory
from exeapp.models.node import Node


def get_package_by_id_or_error(func):
    '''Works on views with package_id argument.
Raises 403 if a package doesn't belong to the user or 404 the package
can't be found. Raises 404 if the node is not in the specified package.
Please specify additional view arguments in the view docstring.
Depends on Http403 handling middleware.
Tested in exeapp.tests.ShortcutsTestCase. '''

    @wraps(func)
    def permission_checking_view(request, package_id, node_id=None, *args,
                                 **kwargs):
        try:
            # assume we got a standard rpc package view
            # if package_id isn't convertable 500 will be thrown
            package_id = int(package_id)
            package = Package.objects.get(pk=package_id)
            node = None
            if node_id is not None:
                try:
                    node_id = int(node_id)
                    node = Node.objects.get(pk=node_id)
                except ObjectDoesNotExist:
                    raise Http404("Node {} not found".format(node_id))
        except ObjectDoesNotExist:
            raise Http404("Package {} not found".format(package_id))
        username = request.user.username
        if package.user == request.user or \
                        request.user in package.collaborators.all():
            if node is not None:
                if node.package == package:
                    return func(request, package, node, *args, **kwargs)
                else:
                    Http404("Requested node not found in package {}". \
                            format(package_id))
            else:
                return func(request, package, *args, **kwargs)
        else:
            raise Http403("User %s may not access package %s" % \
                          (username, package_id))

    # Set docstring and name
    return permission_checking_view


def jsonrpc_authernticating_method(*args, **kwargs):
    """Chains jsonrpc_method and get_package_by_id_or_error decorators"""

    def decorator(func):
        if "authenticated" not in kwargs:
            kwargs['authenticated'] = True

        @jsonrpc_method(*args, **kwargs)
        @get_package_by_id_or_error
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

    return decorator


def render_idevice(idevice):
    """Finds the leaf idevice and renders it"""
    leaf_idevice = idevice.as_child()
    block = block_factory(leaf_idevice)
    return render_to_string("exe/authoring_idevice_form.html",
                            {'block': block})
