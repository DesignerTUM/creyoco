import re
import sys
import wikipedia
from django.db import models
from django.utils.translation import ugettext_lazy as _
from bs4 import BeautifulSoup

from exeapp.models.idevices.genericidevice import GenericIdevice
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices import fields


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
        wikiHTML = page.html()
        self.content = self.process_html (wikiHTML)


    def process_html(self, html):
        soup = BeautifulSoup(html)
        #remove edit buttons from sections
        for edit_span in soup.findAll('span', 'mw-editsection'):
            edit_span.extract()
        return soup.prettify()

    class Meta:
        app_label = "exeapp"
