import wikipedia
from django.db import models
from django.utils.translation import ugettext_lazy as _
from bs4 import BeautifulSoup
from django.utils.text import slugify
import urllib
import os
from exeapp.utils.path import Path

from exeapp.models.idevices.genericidevice import GenericIdevice
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices import fields


'''
PY2 = sys.version_info[0] == 2
try:
    from urllib.request import urlopen, FancyURLopener
    from urllib.parse import quote
except ImportError:
    if PY2:  # python2
        from urllib import quote, FancyURLopener, urlopen
    else:
        raise

try:
    import urllib.request
except ImportError:
    if PY2:
        import urllib
'''

class WikipediaIdevice(GenericIdevice):
    name = _("Wiki Article")
    title = models.CharField(max_length=100, default=name)
    author = _("University of Auckland")
    purpose = _("""<p>The Wikipedia iDevice allows you to locate
existing content from within Wikipedia and download this content into your eXe
resource. The Wikipedia Article iDevice takes a snapshot copy of the article
content. Changes in Wikipedia will not automatically update individual snapshot
copies in eXe, a fresh copy of the article will need to be taken. Likewise,
changes made in eXe will not be updated in Wikipedia. </p> <p>Wikipedia content
is covered by the GNU free documentation license.</p>""")
    emphasis = Idevice.NOEMPHASIS
    group = Idevice.CONTENT
    article_name = fields.URLField(max_length=100, blank=True, default="",
                                   help_text=_("""Enter a phrase or term you
                                   wish to search
within Wikipedia."""))
    language_choices = (('de', 'DE'), ('en', 'EN'))
    #language = models.CharField(max_length=2, choices=language_choices, default='en')
    language = models.CharField(max_length=2, default="en", choices=language_choices)
    content = fields.RichTextField(blank=True, default="")
    site = "wikipedia.org/wiki/"
    icon = "icon_inter.gif"
    userResources = []
    # TODO FDL has to be in the package
    # systemResources += ["fdl.html"]
    # self._langInstruc      = x_(u"""Select the appropriate language version
    # of Wikipedia to search and enter search term.""")

    def _resources(self):
        """Just returns an empty set"""
        return set()


    def load_article(self, title):
        """
        Load the article from Wikipedia
        """
        wikipedia.set_lang(self.language)
        self.article_name = title
        page = wikipedia.page(title)
        page = self.store_images(page)
        self.content = self.process_html (page)


    def process_html(self, html):
        print("process html")
        soup = BeautifulSoup(html)
        soup = self.remove_edit_link(soup)
        #soup = self.store_images(soup)
        return soup.prettify()

    def remove_edit_link(self, soup):
        print("remove edit link")
        for edit_span in soup.findAll('span', 'mw-editsection'):
            edit_span.extract()
        return soup


    def store_images(self,page):
        #for storing files
        local_path = Path.joinpath(Path(self.parent_node.package.user.get_profile().media_path), Path("wiki_cache_images"))
        local_path = Path.joinpath(local_path, Path(self.parent_node.package.id))
        local_path = Path.joinpath(local_path, Path(self.id))

        #for url
        global_path = Path.joinpath(Path(self.parent_node.package.user.get_profile().media_url), Path("wiki_cache_images"))
        global_path = Path.joinpath(global_path, Path(self.parent_node.package.id))
        global_path = Path.joinpath(global_path, Path(self.id))
        #create directory structure
        os.makedirs(local_path)


        soup = BeautifulSoup(page.html())
        #save file and update link in content
        for img in soup.findAll('img'):
            image = "http:"+ img['src']
            filename = img['src'].split('/')[-1]
            filename = slugify(Path._get_namebase(filename)) + Path._get_ext(filename)  #sanitizing filename
            file_path = Path.joinpath(local_path, Path(filename))
            urllib.request.urlretrieve(image, file_path)
            img['src'] = Path.joinpath(global_path, Path.basename(filename))
        #update image hyperlink to wiki for bigger version image
        for image_link in soup.findAll("a", { "class" : "image" }):
            image_link['href'] = "http://wikipedia.org" + image_link['href']

        page = soup.prettify()
        return page

    class Meta:
        app_label = "exeapp"
