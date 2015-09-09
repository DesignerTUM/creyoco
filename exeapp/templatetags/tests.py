import unittest
import sys
from bs4 import BeautifulSoup
from exeapp.templatetags.common import strip_p

from exeapp.templatetags.mainpage_extras import idevice_ul
from exeapp.templatetags.authoring_extras import *
from django import template

if sys.version_info >= (3,):
    from unittest.mock import Mock
else:
    from mock import Mock

PACKAGE_ID = 1


class MainpageExtrasTestCase(unittest.TestCase):

    class Prototype(object):
        '''A mock idevice'''
        def __init__(self, prototype_id, title):
            self.id = prototype_id
            self.__name__ = title.replace(" ", "")
            self.name = title
            self.title = title

    groups = {'Main': [Prototype(1, 'p1'), Prototype(2, 'p2')],
     'Secondary': [Prototype(3, 'p3'), Prototype(4, 'p4')]}
    group_order = ['Secondary', 'Main']

    def test_idevice_ul(self):
        soup = BeautifulSoup(idevice_ul(self.groups, self.group_order))
        self.assertEquals(len(soup.findAll('a')), 6)
        self.assertEquals(len(soup.findAll('li')), 6)
        self.assertEquals(len(soup.findAll('ul')), 2)
        self.assertTrue('Secondary' in soup.find('li').contents[0])

    class Node(object):
        '''A mock node'''
        def __init__(self, id, title, children, current=False):
            self.id = id
            self.title = title
            self.children = Mock()
            self.children.all = Mock(return_value=children)
            self.current = current
            self.package = Mock()
            self.package.id = PACKAGE_ID

        def is_current_node(self):
            return self.current

    class Package(object):
        '''Mock for the package'''
        def __init__(self, root, package_id):
            self.root = root
            self.id = id

    root = Node(1, 'Root',
        [Node(2, 'Child1', [Node(3, 'Grandchild1', []), Node(4, 'Grandchild2', [])]),
        Node(5, 'Child2', [])], current=True)

    package = Package(root, PACKAGE_ID)

    def test_render_outline(self):
        c = template.Context({"package": self.package,
                              "current_package": self.root})

        t = template.Template('''
        {% load mainpage_extras %}
        {% render_outline package current_node %}
        ''')
        output = t.render(c)

        soup = BeautifulSoup(output)
        root = soup.find(attrs={'nodeid': '1'})
        self.assertTrue('Root' in root.contents[0])
        self.assertEquals(len(soup.findAll('li')), 5)
        self.assertEquals(len(soup.findAll('a')), 5)
        self.assertEquals(len(soup.findAll('ul')), 3)

class CommonTestCase(unittest.TestCase):

    def test_strip_p(self):
        output = strip_p("<p><div>Hello</div></p>")
        self.assertEqual(output, "<div>Hello</div>")
        output = strip_p("<p><div>Hello</div><div>Hello2</div></p>")
        self.assertEqual(output, "<div>Hello</div>\n<div>Hello2</div>")