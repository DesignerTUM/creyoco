import re
from urllib.request import unquote

from tinymce.widgets import TinyMCE
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput
from django.template.loader import render_to_string
from django import forms
from bs4 import BeautifulSoup


class FreeTextWidget(TinyMCE):

    def __init__(self, content_language=None, attrs=None, mce_attrs=None, height=None):
        if height is not None:
            style_height = "height: %dpx;" % height
            attrs = attrs or {}
            if "style" in attrs:
                attrs['style'] += style_height
            else:
                attrs['style'] = style_height
        super(FreeTextWidget, self).__init__(content_language,
                                             attrs,
                                             mce_attrs)

    def render_preview(self, content):
        return mark_safe(content)

    def _replace_sources(self, content):
        soup = BeautifulSoup(content)
        imgs = soup.findAll("img")
        for img in imgs:
            if img['src'].startswith(settings.MEDIA_URL):
                img['src'] = img['src'].split("/")[-1]
        objs = soup.findAll("object")
        for obj in objs:
            obj['data'] = obj['data'].split("/")[-1]
            src = obj.find("param", attrs={'name': 'src'})
            src['value'] = src['value'].split("/")[-1]
            flashvars = obj.find("param", attrs={'name': 'flashvars'})
            reg_ex = r'url=.*/(.*?)&.*"'
            flashvars['value'] = re.sub(
                        reg_ex,
                        lambda match: "url=/{}".format(unquote(match.group(1))),
                        flashvars['value'])
        return str(soup)


    def render_export(self, content):
        return self._replace_sources(self.render_preview(content))


class FeedbackWidget(FreeTextWidget):
    media = forms.Media(
            js=["%sscripts/widgets/feedback.js" % settings.STATIC_URL],
            css={"all" : ["%scss/widgets/feedback.css" % \
                          settings.STATIC_URL]})
    js_modules=['feedback']

    def render_preview(self, content):
        return render_to_string("exe/idevices/widgets/feedback.html",
                                {"content": content})


class URLWidget(TextInput):
    def render(self, *args, **kwargs):
        html = super(URLWidget, self).render(*args, **kwargs)
        html += '<input type="submit" name="idevice_action" value="Load" />'
        return html

class ClozeWidget(FreeTextWidget):
    view_media = forms.Media(
            js=["%sscripts/widgets/cloze.js" % settings.STATIC_URL],
            css={"all": ["%scss/widgets/cloze.css" % settings.STATIC_URL]},
    )

    def render_preview(self, content):
        gaps = BeautifulSoup(content).findAll(
            attrs={"style": "text-decoration: underline;"})
        for gap_number, gap in enumerate(gaps):
            content = content.replace(str(gap), '<input type="text" '
                                      'class="cloze_gap"' \
                                      'id="gap_%s" autocomplete="off" />'
                                      % gap_number)

        gaps_text = enumerate((gap.text for gap in gaps))
        return render_to_string("exe/idevices/widgets/cloze.html",
                                {"content" : content,
                                 "gaps_text" : gaps_text})


class MultiChoiceOptionWidget(FreeTextWidget):
    media = forms.Media(
        css={"all": ["{}css/widgets/multichoiceoption.css".format(
            settings.STATIC_URL
        )]}
    )
    js_modules = ['multichoice']

    def render_preview(self, content):
        return render_to_string("exe/idevices/widgets/multichoiceoption.html",
                                {"content": content, "widget": self.attrs})
