# -*- coding: utf-8 -*-
"""
This file contains the tests for important views in exedjango.
Notice, that your tests should always clear package_storage shoudl be cleared,
to prevent conflicts with package creation in another tests. You can use
_clean_up_database_and_store for it.
"""

import os
import sys
from exeapp.utils.path import Path

PY2 = sys.version_info[0] == 2
try:
    from unittest import mock
    from unittest.mock import Mock
except ImportError:
    if PY2:
        import mock
        from mock import Mock
    else:
        raise

from django.test import TestCase, Client
import json
from django.utils.encoding import smart_text
from django.utils.html import escape
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseForbidden, QueryDict
from jsonrpc.proxy import TestingServiceProxy

from exeapp.models import User, Package
from exeapp.views.export.websiteexport import WebsiteExport
from exeapp import shortcuts
from exeapp.shortcuts import get_package_by_id_or_error
from exedjango.base.http import Http403
from exeapp.views.export.websitepage import WebsitePage
from django.core.urlresolvers import reverse
from exeapp.models.idevices.idevice import Idevice
from exeapp.views.package import PackagePropertiesForm
from exeapp.views.export.imsexport import IMSExport
import random
from exeapp.models.idevices.freetextidevice import FreeTextIdevice
from exeapp.models.node import Node
from exeapp.views.export.scormexport import ScormExport, COMMONCARTRIDGE, \
    SCORM12, SCORM2004
from exeapp.views.blocks.blockfactory import block_factory
from bs4 import BeautifulSoup
from django.utils.translation import ugettext_lazy as _


PACKAGE_COUNT = 3
PACKAGE_NAME_TEMPLATE = '%s\'s Package %s'
TEST_USER = "test_admin"
TEST_PASSWORD = "password"


def _create_packages(user, package_count=PACKAGE_COUNT,
                     package_name_template=PACKAGE_NAME_TEMPLATE):
    for counter in range(package_count):
        Package.objects.create(title=package_name_template % (user.username,
                                                              counter),
                               user=user)


def create_basic_database():
    '''Creates 3 users (admin, user) with 5 packages each for testing'''
    if not os.path.exists(settings.MEDIA_ROOT):
        os.mkdir(settings.MEDIA_ROOT)
    admin = User.objects.create_superuser(username=TEST_USER,
                                          email='admin@exe.org',
                                          password=TEST_PASSWORD)
    admin.save()
    user = User.objects.create_user(username='user', email='admin@exe.org',
                                    password='user')
    user.save()
    _create_packages(admin)
    _create_packages(user)


class MainPageTestCase(TestCase):
    def setUp(self):
        create_basic_database()
        self.c = Client()
        # login
        self.c.login(username=TEST_USER, password=TEST_PASSWORD)
        self.s = TestingServiceProxy(self.c,
                                     reverse("jsonrpc_mountpoint"),
                                     version="2.0")

    def tearDown(self):
        User.objects.all().delete()

    def test_basic_elements(self):
        response = self.c.get('/exeapp/')
        self.assertContains(response, _("Overview"))
        self.assertContains(response, "creyoco")

    def test_create_package(self):
        package_name = '%s Package post' % TEST_USER
        self.s.main.create_package(package_name)
        p = Package.objects.get(title=package_name)
        self.assertTrue(p.user.username == TEST_USER)

    def test_require_login(self):
        self.c.logout()
        response = self.c.get('/exeapp/main')
        self.assertFalse('Main Page' in smart_text(response.content))


class PackagesPageTestCase(TestCase):
    PAGE_URL = '/exeapp/package/%s/%s/'
    PACKAGE_ID = 1
    NODE_ID = 1

    def setUp(self):
        self.c = Client()
        create_basic_database()
        self.c.login(username=TEST_USER, password=TEST_PASSWORD)
        self.s = TestingServiceProxy(self.c,
                                     reverse("jsonrpc_mountpoint"),
                                     version="2.0")

    def tearDown(self):
        User.objects.all().delete()

    def test_basic_structure(self):
        response = self.c.get(self.PAGE_URL % (self.PACKAGE_ID, self.NODE_ID))
        package_title = Package.objects.get(id=self.PACKAGE_ID).title
        self.assertContains(response, escape(package_title))

    def test_outline_pane(self):
        response = self.c.get(self.PAGE_URL % (self.PACKAGE_ID,
                                               self.NODE_ID))
        self.assertContains(response, "outline_pane")
        self.assertContains(response, 'current_node="%s"' % self.NODE_ID)

    @mock.patch.object(Package.objects, 'get')
    @mock.patch.object(Node.objects, 'get')
    def test_rpc_calls(self, mock_node_get, mock_package_get):
        NODE_ID = 42
        NODE_TITLE = "Node"
        PARENT_ID = 1
        PARENT_TITLE = "Parent"

        # mock node
        new_node = Mock()
        new_node.id = NODE_ID
        new_node.title = NODE_TITLE

        parent_node = Mock()
        parent_node.id = PARENT_ID
        parent_node.title = PARENT_TITLE
        parent_node.create_child.return_value = new_node
        parent_node.collaborators.all.return_value = []

        # mock package
        package = Mock()
        package.user = User.objects.get(username=TEST_USER)
        package.collaborators.all.return_value = []

        # mock get query
        mock_node_get.return_value = parent_node
        mock_package_get.return_value = package
        parent_node.package = package

        r = self.s.package.add_child_node(
            # username=TEST_USER,
            # password=TEST_PASSWORD,
            package_id="1",
            node_id=str(PARENT_ID))
        result = r['result']
        self.assertEquals(result['id'], NODE_ID)
        self.assertEquals(result['title'], NODE_TITLE)
        self.assertTrue(parent_node.create_child.called)

    def test_idevice_pane(self):
        response = self.c.get(self.PAGE_URL % (self.PACKAGE_ID, self.NODE_ID))
        self.assertContains(response, "outline_pane")
        self.assertContains(response, _("Free Text"))

    def test_authoring(self):
        response = self.c.get(self.PAGE_URL % (self.PACKAGE_ID,
                                               self.NODE_ID),
                              HTTP_X_PJAX='True')
        self.assertContains(response, "package_id")
        self.assertContains(response, "node_id")
        self.assertContains(response, self.PACKAGE_ID)
        self.assertContains(response, self.NODE_ID)

    def test_404_on_wrong_package(self):
        # # this id shouldn't be created
        WRONG_PACKAGE_ID = PACKAGE_COUNT * 2 + 1
        response = self.c.get(self.PAGE_URL % (WRONG_PACKAGE_ID, self.NODE_ID))
        self.assertTrue(isinstance(response, HttpResponseNotFound))

    def test_403_on_wrong_user(self):
        USERS_PACKAGE_ID = PACKAGE_COUNT + 1
        response = self.c.get(self.PAGE_URL % (USERS_PACKAGE_ID, self.NODE_ID))
        self.assertTrue(isinstance(response, HttpResponseForbidden))

    def test_properties(self):
        '''Test if the properties page is rendered propertly'''
        response = self.c.get(self.PAGE_URL % (self.PACKAGE_ID, self.NODE_ID))
        self.assertContains(response, 'properties_form')

    def test_change_properties(self):
        AUTHOR_NAME = "Meeee"
        PACKAGE_TITLE = "Sample_Title"

        response = self.c.post(self.PAGE_URL % (self.PACKAGE_ID, self.NODE_ID),
                               data={'title': PACKAGE_TITLE,
                                     'author': AUTHOR_NAME,
                                     'form_type_field': PackagePropertiesForm.
                               form_type})
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response['location'].endswith(
            self.PAGE_URL % (self.PACKAGE_ID, self.NODE_ID)))
        package = Package.objects.get(id=self.PACKAGE_ID)
        self.assertTrue(package.author == AUTHOR_NAME)
        self.assertTrue(package.title == PACKAGE_TITLE)

    def test_preview(self):
        response = self.c.get("{}preview/".format(self.PAGE_URL %
                                                  (self.PACKAGE_ID,
                                                   self.NODE_ID)))
        self.assertContains(response, "Home", status_code=200)


class ShortcutTestCase(TestCase):
    PACKAGE_ID = 1
    NON_EXISTENT_PACKAGE_ID = 9001  # over 9000
    PACKAGE_TITLE = "test"
    TEST_USER = 'test_admin'
    WRONG_USER = 'foo'
    TEST_PASSWORD = 'admin'
    TEST_ARG = 'arg'

    @mock.patch.object(Package.objects, 'get')
    def test_get_package_or_error(self, mock_get):
        '''Tests exeapp.shortcuts.get_package_by_id_or_error convinience
decorator'''

        # mock request
        request = Mock()
        request.user = User.objects.create_user(username=self.TEST_USER,
                                                password="pass")

        # mock package
        package = Mock()
        wrong_user = User.objects.create_user(username=self.WRONG_USER,
                                              password="pass")
        package.user = wrong_user
        package.collaborators.all.return_value = []

        # mock getter
        mock_get.return_value = package

        @get_package_by_id_or_error
        def mock_view(request, package):
            return package

        self.assertRaises(Http403, mock_view, request,
                          self.PACKAGE_ID)
        mock_get.assert_called_with(pk=self.PACKAGE_ID)

    @mock.patch.object(Package.objects, 'get')
    @mock.patch.object(Node.objects, 'get')
    def package_and_node_or_error(self, mock_get_package, mock_get_node):
        """Tests exeapp.shortcuts.get_package_by_id_or_error with package
        and node"""
        NODE_ID = 1

        request = Mock()
        request.user.username = self.TEST_USER

        package = Mock()
        package.user.username = self.TEST_USER

        wrong_package = Mock()

        node = Mock()
        node.package = wrong_package
        node.id = NODE_ID

        mock_get_package.return_value = package
        mock_get_node.return_value = node

        @get_package_by_id_or_error
        def mock_view(request, package, node):
            return package

        self.assertRaises(Http403, mock_view, request,
                          self.PACKAGE_ID, NODE_ID)
        mock_get_package.assert_called_with(pk=self.PACKAGE_ID)
        mock_get_node.assert_called_with(pk=NODE_ID)


class AuthoringTestCase(TestCase):
    '''Tests the authoring view. The it ill be brought together with package
view, this tests should be also merged'''

    TEST_PACKAGE_ID = 1
    TEST_NODE_ID = 1
    TEST_NODE_TITLE = "Home"
    IDEVICE_TYPE = "FreeTextIdevice"

    VIEW_URL = "/exeapp/package/%s/%s/" % \
               (TEST_PACKAGE_ID, TEST_NODE_ID)

    def setUp(self):
        self.c = Client()
        create_basic_database()
        self.c.login(username=TEST_USER, password=TEST_PASSWORD)
        self.s = TestingServiceProxy(self.c,
                                     reverse("jsonrpc_mountpoint"),
                                     version="2.0")
        self.package = Package.objects.get(pk=self.TEST_PACKAGE_ID)
        self.root = self.package.root

    def tearDown(self):
        User.objects.all().delete()

    def test_basic_elements(self):
        '''Basic tests aimed to determine if this view works at all'''
        response = self.c.get(self.VIEW_URL)
        soup = BeautifulSoup(response.content)
        self.assertEqual(int(soup.find("div", {'id': 'package_id'}).text),
                         self.TEST_PACKAGE_ID)
        self.assertEqual(int(soup.find("div", {'id': 'node_id'}).text),
                         self.TEST_NODE_ID)
        #
        # self.assertContains(response, 'Package %s' % self
        # .TEST_PACKAGE_ID)
        #        self.assertContains(response,
        #            """<div id="node_id" style="display: none">{}</div>"""
        # .format(
        #                                                         self
        # .TEST_NODE_ID))
        self.assertContains(response, self.TEST_NODE_TITLE)

    def test_idevice(self):
        '''Tests if idevice is rendered properly'''
        IDEVICE_ID = 1

        self.root.add_idevice(self.IDEVICE_TYPE)
        response = self.c.get(self.VIEW_URL)
        self.assertContains(response, 'idevice_id="%s"' % IDEVICE_ID)

    def test_post_page_change(self):
        TEST_TITLE = "Test"

        response = self.c.post(self.VIEW_URL,
                               {
                                   'form_type_field': PackagePropertiesForm
                               .form_type,
                                   'title': TEST_TITLE
                               })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response['Location'].endswith(
            'exeapp/package/{}/{}/'.format(
                self.package.id,
                self.package.root.id
            )
        )
        )

    def test_idevice_move_up(self):
        FIRST_IDEVICE_ID = 1
        SECOND_IDEVICE_ID = 2
        self.root.add_idevice(self.IDEVICE_TYPE)
        self.root.add_idevice(self.IDEVICE_TYPE)
        self.package.root.handle_action(SECOND_IDEVICE_ID,
                                        "move_up",
                                        QueryDict(""))
        content = smart_text(self.c.get(self.VIEW_URL).content)
        self.assertTrue(content.index(
            'idevice_id="{}"'.format(FIRST_IDEVICE_ID))
                        > content.index(
            'idevice_id="{}"'.format(SECOND_IDEVICE_ID)))

    @mock.patch.object(shortcuts, 'render_idevice')
    @mock.patch.object(Package.objects, 'get')
    @mock.patch.object(Node.objects, 'get')
    def test_submit_idevice_action(self, mock_node_get, mock_package_get,
                                   mock_render):
        '''Test if a POST request is delegated to package'''
        idevice_id = "1"
        idevice_action = "save"
        mock_package_get.return_value.user = User.objects.get(
            username=TEST_USER)
        mock_node_get.return_value.package = mock_package_get.return_value
        action_args = {"test": "a", "test2": "1",
                       'idevice_id': idevice_id,
                       'idevice_action': idevice_action}

        def mock_render_idevice(idevice):
            return idevice.content

        mock_render.side_effect = mock_render_idevice

        response = self.c.post('%shandle_action/' % self.VIEW_URL,
                               data=action_args)
        self.assertEquals(response.status_code, 200)
        test_args = QueryDict("").copy()
        test_args.update(action_args)
        mock_node_get.return_value.handle_action.assert_called_with(
            str(idevice_id),
            "save",
            test_args)

    def test_idevice_link_list(self):
        IDEVICE_ID = 1
        ANCHORS = ("anchor1", "anchor2")

        self.root.add_idevice(self.IDEVICE_TYPE)
        idevice = FreeTextIdevice.objects.get(id=IDEVICE_ID)
        idevice.content = '<a name="%s"></a><a name="%s"></a>' % ANCHORS
        link_list = idevice.link_list
        counter = 0
        for anchor in ANCHORS:
            name, url = link_list[counter]
            self.assertEquals(name, "%s::%s" %
                              (idevice.parent_node.title, anchor))
            self.assertEquals(url, "%s.html#%s" %
                              (idevice.parent_node.unique_name(), anchor))
            counter += 1

    @mock.patch.object(shortcuts, 'render_idevice')
    @mock.patch.object(Package.objects, 'get')
    @mock.patch.object(Node.objects, 'get')
    def test_render_idevice_partial(self, mock_node_get,
                                    mock_package_get,
                                    mock_render):
        '''Test rendering of a single idevice if idevice_id is given'''
        IDEVICE_ID = 1
        IDEVICE_CONTENT = "Test idevice"
        # patch render_idevice

        def mock_render_idevice(idevice):
            return idevice.content

        mock_render.side_effect = mock_render_idevice

        package = mock_package_get.return_value
        package.user = User.objects.get(username=TEST_USER)

        node = mock_node_get.return_value
        node.package = package

        node.idevices.get.return_value.content = IDEVICE_CONTENT

        response = self.c.get(self.VIEW_URL + "authoring/",
                              data={"idevice_id": IDEVICE_ID})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(node.idevices.get.called)
        self.assertTrue(IDEVICE_CONTENT in smart_text(response.content))

    def test_partial_resource_loading(self):
        self.root.add_idevice(self.IDEVICE_TYPE)
        response = self.c.get("{}authoring/?partial=true&media=true".format(
            self.VIEW_URL))
        self.assertIn(
            reverse('tinymce-filebrowser'),
            json.loads(smart_text(response.content))['js']
        )

    def test_resource_finding(self):
        RESOURCE = 'test.jpg'
        CONTENT = '<img src="/media/uploads/%s/%s" />' % \
                  (self.package.user.username, RESOURCE)
        IDEVICE_ID = 1

        self.root.add_idevice(self.IDEVICE_TYPE)
        test_idevice = Idevice.objects.get(id=IDEVICE_ID).as_child()
        test_idevice.content = CONTENT
        self.assertEquals(test_idevice.resources, set([RESOURCE]))

    def test_export_resource_substitution(self):
        RESOURCE = 'test.jpg'
        CONTENT = 'src="/exeapp/media/uploads/%s/%s"' % (
            self.package.user.username,
            RESOURCE)
        IDEVICE_ID = 1

        self.root.add_idevice(self.IDEVICE_TYPE)
        test_idevice = Idevice.objects.get(id=IDEVICE_ID).as_child()
        test_idevice.content = CONTENT
        test_block = block_factory(test_idevice)
        self.assertTrue(RESOURCE in test_block.renderView())

    def test_idevice_factory(self):
        IDEVICE_ID = 1

        self.root.add_idevice(self.IDEVICE_TYPE)
        test_idevice = Idevice.objects.get(id=IDEVICE_ID).as_child()
        block = block_factory(test_idevice)
        self.assertTrue("<textarea" in block.renderEdit())

    def test_link_list(self):
        response = self.c.get('{}{}'.format(self.VIEW_URL, settings.LINK_LIST))
        self.assertContains(response, 'tinyMCELinkList')
        try:
            # remove trailing semi-colon at the end
            link_list = smart_text(response.content).split('=')[-1][:-1]
        except IndexError:
            raise AssertionError("Couldn't find link array in {}".format(
                response.content))
        try:
            json.loads(link_list)
        except:
            raise AssertionError("Couldn't parse %s" % link_list)

    def test_style_invalid(self):
        self.assertRaises(ValueError, self.s.package.set_package_style,
                          1, 1, 'BS')


class ExportTestCase(TestCase):
    TEST_PACKAGE_ID = 1
    IDEVICE_TYPE = "FreeTextIdevice"

    def setUp(self):
        create_basic_database()
        self.data = Package.objects.get(id=self.TEST_PACKAGE_ID)
        for x in range(3):
            self.data.root.create_child()

    def tearDown(self):
        User.objects.all().delete()

    def test_basic_export(self):
        '''Exports a package'''

        exporter = WebsiteExport(self.data, settings.MEDIA_ROOT + "/111.zip")
        exporter.export()

    def test_ims_export(self):
        '''Exports a package'''

        self.data.root.add_idevice(self.IDEVICE_TYPE)
        exporter = IMSExport(self.data, settings.MEDIA_ROOT + "/111.zip")
        exporter.export()

    def test_scorm_export(self):
        '''Exports a package'''

        self.data.root.add_idevice(self.IDEVICE_TYPE)
        scorm_types = [SCORM12, SCORM2004, COMMONCARTRIDGE]
        for scorm_type in scorm_types:
            exporter = ScormExport(self.data, settings.MEDIA_ROOT + "/111.zip",
                                   scorm_type=scorm_type)
            exporter.export()

    def test_pages_generation(self):
        '''Tests generation of the page nested list'''

        class MockNode(object):
            def __init__(self, title):
                self.id = random.randint(1, 100)
                self.title = title
                self.children = MockQuerySet([])
                self.is_root = False
                self.idevices = Mock()
                self.idevices.all.return_value = []

            def unique_name(self):
                return "%s_%s" % (self.title, self.id)

        class MockQuerySet(object):
            def __init__(self, values):
                self.values = values

            def all(self):
                return self.values

            def exists(self):
                return bool(self.values)

        nodes = [MockNode("Node%s" % x) for x in range(4)]
        nodes[0].is_root = True
        nodes[0].children = MockQuerySet([nodes[1], nodes[2]])
        nodes[2].children = MockQuerySet([nodes[3]])
        mock_exporter = WebsiteExport(Mock(), Mock())
        mock_exporter.generate_pages(nodes[0], 1)
        pages = mock_exporter.pages
        pages.insert(0, None)
        pages.append(None)
        for i in range(1, len(pages) - 1):
            page = pages[i]

            if i != 0:
                self.assertEquals(page.prev_page, pages[i - 1])
            if i != len(pages):
                self.assertEquals(page.next_page, pages[i + 1])

    def test_websitepage(self):
        IDEVICE_TYPE = "FreeTextIdevice"

        self.data.root.add_idevice(IDEVICE_TYPE)
        exporter = Mock()
        exporter.pages = []
        exporter.style_dir = Path(settings.STATIC_ROOT) / "css" / "styles" / "bmz"
        websitepage = WebsitePage(self.data.root, 0, exporter)
        exporter.pages.append(websitepage)
        self.assertTrue('class="%s" id="id1"' % IDEVICE_TYPE
                        in websitepage.render())


class MiddleWareTestCase(TestCase):
    def test_403_middleware(self):
        '''Test the HTTP403 handlingmiddle ware.
Should set status code to 403'''
        from django.conf.urls import patterns
        from exeapp.urls import urlpatterns
        from exeapp import views

        # patch new test view which raises Http403
        views.test = Mock()
        views.test.side_effect = Http403
        urlpatterns += patterns('',
                                ("test/$", 'exeapp.views.test'))
        c = Client()
        response = c.get('/exeapp/test/')
        self.assertEquals(response.status_code, 403)


class OutlineTestCase(TestCase):
    """Tests basic outline function"""

    TEST_PACKAGE_ID = 1

    def setUp(self):
        create_basic_database()
        self.data = Package.objects.get(id=self.TEST_PACKAGE_ID)
        self.c = Client()
        self.c.login(username=TEST_USER, password=TEST_PASSWORD)
        self.s = TestingServiceProxy(self.c,
                                     reverse("jsonrpc_mountpoint"),
                                     version="2.0")
        for x in range(3):
            self.data.root.create_child()

    def tearDown(self):
        User.objects.all().delete()

    def test_add_node(self):
        PARENT_ID = Node.objects.all()[0].pk
        r = self.s.package.add_child_node(
            # username=TEST_USER,
            # password=TEST_PASSWORD,
            package_id="1",
            node_id=str(PARENT_ID))
        self.assertEqual(r['result']['title'], Package.DEFAULT_LEVEL_NAMES[0])

    def test_add_node_with_title(self):
        PARENT_ID = Node.objects.all()[0].pk
        NODE_TITLE = "Test title"
        r = self.s.package.add_child_node(
            # username=TEST_USER,
            # password=TEST_PASSWORD,
            package_id="1",
            node_id=str(PARENT_ID),
            new_name=NODE_TITLE)
        self.assertEqual(r['result']['title'], NODE_TITLE)

    def test_duplicated_node(self):
        parent = Node.objects.all()[0]
        test_child = Node.objects.create(self.data, parent, "Test Child")
        old_child_number = len(parent.children.all())
        r = self.s.package.duplicate_node(
            package_id="1",
            node_id=test_child.pk,
        )
        self.assertEqual(len(parent.children.all()), old_child_number + 1)
        self.assertIsNotNone(r['result'])
        self.assertTrue('id' in r['result'])
        new_id = r['result']['id']
        self.assertTrue('title' in r['result'])
        self.assertEqual(Node.objects.get(pk=new_id).title, test_child.title)
        self.assertEquals(r['result']['title'], test_child.title)
