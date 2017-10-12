import sys
import re

from ckeditor.widgets import CKEditorWidget
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput
from django.template.loader import render_to_string
from django import forms
from bs4 import BeautifulSoup


if sys.version_info >= (3,):
    from urllib.request import unquote
else:
    from urllib import unquote


class FreeTextWidget(CKEditorWidget):

    @property
    def media(self):
        media = self.__class__.Media()
        js = list(media.js)
        # try:
        #     js.remove(settings.CKEDITOR_JQUERY_URL)  # we already load jquery
        # except ValueError:
        #     # jquery doesn't have to be in the path
        #     pass
        return forms.Media(
        js=js,
        css={"all": []})

    js_modules = []

    def __init__(self, config_name='creyoco', content_language=None, attrs=None, mce_attrs=None,
                 height=None):
        if height is not None:
            style_height = "height: %dpx;" % height
            attrs = attrs or {}
            if "style" in attrs:
                attrs['style'] += style_height
            else:
                attrs['style'] = style_height
        super(FreeTextWidget, self).__init__(config_name, content_language,
                                             attrs,
                                             mce_attrs)

    def render_preview(self, content):
        return mark_safe(content)

    def _replace_sources(self, content):
        soup = BeautifulSoup(content)
        resource_holders = soup.findAll(["img", "a", "video"])
        for holder in resource_holders:
            if holder.name == "img":
                if holder['src'].startswith(settings.MEDIA_URL):
                    holder['src'] = holder['src'].split("/")[-1]
            elif holder.name == "a":
                if holder.has_key('href') and holder['href'].startswith(settings.MEDIA_URL):
                    holder['href'] = holder['href'].split("/")[-1]
            elif holder.name == "video":
                video_sources = holder.findAll('source')
                for video_source in video_sources:
                    if video_source['src'].startswith(settings.MEDIA_URL):
                        video_source['src'] = video_source['src'].split("/")[-1]
        objs = soup.findAll("object")
        for obj in objs:
            obj['data'] = obj['data'].split("/")[-1]
            src = obj.find("param", attrs={'name': 'src'})
            src['value'] = src['value'].split("/")[-1]
            flashvars = obj.find("param", attrs={'name': 'flashvars'})
            reg_ex = r'url=.*/(.*?)&.*'
            flashvars['value'] = re.sub(
                reg_ex,
                lambda match: "url=./{}".format(
                    unquote(match
                            .group(1)
                            .replace(settings.MEDIA_URL, '')
                    )
                ),
                flashvars['value'])
        return str(soup)


    def render_export(self, content):
        return self._replace_sources(self.render_preview(content))


class FeedbackWidget(FreeTextWidget):
    media = forms.Media(
        js=["%sscripts/widgets/feedback.js" % settings.STATIC_URL],
        css={"all": ["%scss/widgets/feedback.css" % \
                     settings.STATIC_URL]})
    js_modules = ['feedback']

    def render_preview(self, content):
        return render_to_string("exe/idevices/widgets/feedback.html",
                                {"content": content})


class URLWidget(TextInput):
    def render(self, *args, **kwargs):
        html = super(URLWidget, self).render(*args, **kwargs)
        html += '<input type="submit" name="idevice_action" value="Load" />'
        return html


class ClozeWidget(FreeTextWidget):
    media = forms.Media(
        js=["{}scripts/widgets/cloze.js".format(settings.STATIC_URL)],
        css={"all": ["{}css/widgets/cloze.css".format(
            settings.STATIC_URL)
        ]},
    )
    js_modules = ['cloze']

    def render_preview(self, content):
        soup = BeautifulSoup(content)
        gaps = soup.findAll("u")
        gaps += soup.findAll(
            attrs={"style": "text-decoration: underline;"})
        for gap_number, gap in enumerate(gaps):
            content = content.replace(str(gap), '<span contenteditable="true"'
                                                'class="cloze_gap"' \
                                                'id="gap_%s" '
                                                'autocomplete="off"></span>'
                                      % gap_number)

        gaps_text = enumerate((gap.text for gap in gaps))
        return render_to_string("exe/idevices/widgets/cloze.html",
                                {"content": content,
                                 "gaps_text": gaps_text})


class MultiChoiceOptionWidget(FreeTextWidget):
    media = forms.Media(
        js=["{}scripts/blocks/multichoice.js".format(settings.STATIC_URL)],
        css={"all": ["{}css/widgets/multichoiceoption.css".format(
            settings.STATIC_URL
        )]}
    )
    js_modules = ['multichoice']

    def render_preview(self, content):
        return render_to_string("exe/idevices/widgets/multichoiceoption.html",
                                {"content": content, "widget": self.attrs})
