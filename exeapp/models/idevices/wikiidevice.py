import re
import sys

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


class UrlOpener(FancyURLopener):
    """
    Set a distinctive User-Agent, so Wikipedia.org knows we're not spammers
    """
    version = "eXe/exe@exelearning.org"


try:
    import urllib.request

    urllib.request._urlopener = UrlOpener()
except ImportError:
    if PY2:
        import urllib

        urllib._urlopener = UrlOpener()


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
    content = fields.RichTextField(blank=True, default="")
    site = "http://en.wikipedia.org/wiki/"
    icon = "icon_inter.gif"
    userResources = []
    # TODO FDL has to be in the package
    # systemResources += ["fdl.html"]
    #    self._langInstruc      = x_(u"""Select the appropriate language version
    # of Wikipedia to search and enter search term.""")

    def load_article(self, title):
        """
        Load the article from Wikipedia
        """
        self.articleName = title
        url = ""
        title = urllib.parse.quote(title.replace(" ", "_").encode('utf-8'))
        try:
            url = (self.site or self.ownUrl)
            if not url.endswith('/') and title != '': url += '/'
            if '://' not in url: url = 'http://' + url
            url += title
            net = urllib.request.urlopen(url)
            page = net.read()
            net.close()
        except IOError as error:
            self.content = _(
                "Unable to download from %s <br/>Please check the spelling "
                "and connection and try again.") % url
            return

        # FIXME avoid problems with numeric entities in attributes
        page = page.replace('&#160;', '&nbsp;')

        soup = BeautifulSoup(page)
        content = soup.find('div', {'id': "content"})

        # remove the wiktionary, wikimedia commons, and categories boxes
        #  and the protected icon and the needs citations box
        print(content)
        if content:
            content['id'] = 'wiki_content'
            infoboxes = content.findAll('div',
                                        {'class': 'infobox sisterproject'})
            [infobox.extract() for infobox in infoboxes]
            catboxes = content.findAll('div', {'id': 'catlinks'})
            [catbox.extract() for catbox in catboxes]
            amboxes = content.findAll('table',
                                      {'class': re.compile(r'.*\bambox\b.*')})
            [ambox.extract() for ambox in amboxes]
            protecteds = content.findAll('div', {'id': 'protected-icon'})
            [protected.extract() for protected in protecteds]
        else:
            content = soup.first('body')

        if not content:
            self.content = _(
                "Unable to download from %s <br/>Please check the spelling "
                "and connection and try again.") % url
            # set the other elements as well
            return

        bits = url.split('/')
        netloc = '%s//%s' % (bits[0], bits[2])
        self.content = self.reformatArticle(netloc, content)
        # now that these are supporting images, any direct manipulation
        # of the content field must also store this updated information
        # into the other corresponding fields of TextAreaField:
        # (perhaps eventually a property should be made for TextAreaField
        #  such that these extra set's are not necessary, but for now, here:)

    def reformatArticle(self, netloc, content):
        """
        Changes links, etc
        """
        content = re.sub(r'href="/', r'href="%s/' % netloc, content)
        content = re.sub(
            r'<(span|div)\s+(id|class)="(editsection|jump-to-nav)".*?</\1>', '',
            content)
        # TODO Find a way to remove scripts without removing newlines
        content = content.replace("\n", " ")
        content = re.sub(r'<script.*?</script>', '', content)
        return content

    class Meta:
        app_label = "exeapp"




