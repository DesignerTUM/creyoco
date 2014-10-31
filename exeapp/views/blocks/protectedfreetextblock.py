import urllib
from django.forms import forms
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
import itertools
from exeapp.models import Idevice
from exeapp.views.blocks.freetextblock import FreeTextBlock
from exeapp.views.blocks.genericblock import GenericBlock, TemplateNotDefined


class ProtectedFreeTextBlock(FreeTextBlock):
    # use_common_content = True

    edit_template = "exe/idevices/protectedfreetext/edit.html"
    preview_template = "exe/idevices/protectedfreetext/preview.html"
    view_template = "exe/idevices/protectedfreetext/export.html"

    def _render_view(self, template, form=None):
        """
        Code reuse function for rendering the correct template
        """
        form = form or self.BlockForm(instance=self.idevice,
                                      auto_id="%s_field_" % self.idevice.id +
                                              "%s")
        try:
            html = render_to_string(template, {"form": form,
                                               "block_ref": self,
                                               "idevice": self.idevice
                                                }
                                    )
        except TemplateDoesNotExist as e:
            if template:
                raise e
            else:
                raise TemplateNotDefined(
                    "Please define a template for the action")
        else:
            return html

    def xor(self, data=None, key=None):
        if data is None:
            data = self.idevice.content
        if key is None:
            key = self.idevice.password
        data = data + "proof"   #proof is for checking if pw is right after decrypting
        return urllib.parse.quote(''.join(chr(ord(k) ^ ord(c)) for c,k in zip(data, itertools.cycle(key))))

    @property
    def media(self):
        return forms.Media(js=['{}scripts/blocks/protectedfreetext.js'.format(settings.STATIC_URL)],
                           css={'all': ['{}css/blocks/protectedfreetext.css' \
                             .format(settings.STATIC_URL)]})
