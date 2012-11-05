from exeapp.views.blocks.formsetblock import BaseFormsetBlock,\
    FormsetBlockMetaclassFactory
from exeapp.models.idevices.glossaryidevice import GlossaryTerm
from django.template.loader import render_to_string

class GlossaryBlock(BaseFormsetBlock):
    __metaclass__ = FormsetBlockMetaclassFactory(
                                GlossaryTerm,
                                ("title", "definition"))
    
    preview_template = "exe/idevices/glossary/preview.html"
    view_template = "exe/idevices/glossary/export.html"
    
    def renderPreview(self):
        ordered_terms = self.idevice.terms.order_by('title')
        return render_to_string(self.preview_template, 
                                {"idevice" : self.idevice,
                                 "ordered_terms" : ordered_terms,
                                 "self" : self,
                                 }
                                )
    
    def renderView(self):
        ordered_terms = self.idevice.terms.order_by('title')
        return render_to_string(self.view_template,
                                 {"idevice" : self.idevice,
                                  "ordered_terms" : ordered_terms,
                                  }
                                )