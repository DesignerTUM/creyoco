from tinymce.widgets import TinyMCE
from django.conf import settings
from django.utils.safestring import mark_safe
import re
from django.utils.html import escape
from django.forms.widgets import TextInput
from django.template.loader import render_to_string
from django import forms
from django.core.urlresolvers import reverse
from BeautifulSoup import BeautifulSoup

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
        reg_exp = r'src=".*%s.*/(.*?)"' % settings.MEDIA_URL
        return re.sub(reg_exp, r'src="\g<1>"', content)

    def render_export(self, content):
        return self._replace_sources(self.render_preview(content))


class FeedbackWidget(FreeTextWidget):
    view_media = forms.Media(
            js=["%sscripts/widgets/feedback.js" % settings.STATIC_URL],
            css={"all" : ["%scss/widgets/feedback.css" % \
                          settings.STATIC_URL]})

    def render_preview(self, content):
        return render_to_string("exe/idevices/widgets/feedback.html",
                                {"content" : content})


class URLWidget(TextInput):
    def render(self, *args, **kwargs):
        html = super(URLWidget, self).render(*args, **kwargs)
        html += '<input type="submit" name="idevice_action" value="Load" />'
        return html

class ClozeWidget(FreeTextWidget):
    view_media = forms.Media(
            js=["%sscripts/widgets/cloze.js" % settings.STATIC_URL],
            css={"all" : ["%scss/widgets/cloze.css" % settings.STATIC_URL]},
                    )
    def render_preview(self, content):
        gaps = BeautifulSoup(content).findAll(attrs={"style" : "text-decoration: underline;"})
        for gap_number, gap in enumerate(gaps):
            content = content.replace(str(gap), '<input type="text" '
                                      'class="cloze_gap"' \
                                      'id="gap_%s" autocomplete="off" />'
                                      % gap_number)

        gaps_text = enumerate((gap.text for gap in gaps))
        return render_to_string("exe/idevices/widgets/cloze.html",
                                {"content" : content,
                                 "gaps_text" : gaps_text})
