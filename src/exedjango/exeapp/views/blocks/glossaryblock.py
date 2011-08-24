from exedjango.exeapp.views.blocks.ideviceform import IdeviceForm
from django.utils.safestring import mark_safe

class GlossaryTermForm(IdeviceForm):
    
    def _render_view(self, purpose):
        html = "<em>%s</em>%s" %\
            (self.initial['title'], self.initial['definition'])
        return mark_safe(html)
        

    
