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

    edit_template = "exe/idevices/freetext/edit.html"
    preview_template = "exe/idevices/generic/preview.html"

    def _render_view(self, template, form=None):
        """
        Code reuse function for rendering the correct template
        """
        temp_idevice = self.idevice
        temp_idevice.content = self.xor(temp_idevice.content, self.idevice.password)
        form = form or self.BlockForm(instance=self.idevice,
                                      auto_id="%s_field_" % self.idevice.id +
                                              "%s")
        try:
            html = render_to_string(template, {"idevice": temp_idevice,
                                               "form": form,
                                               "content_template": self
                                               .content_template,
                                               "self": self,
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

    def xor(self, data, key):
        return ''.join(chr(ord(k)^ord(c)) for c,k in zip(data,itertools.cycle(key)))

    @property
    def media(self):
        return forms.Media(js=['{}scripts/blocks/protectedfreetext.js'.format(settings.STATIC_URL)])
