from django import forms
from django.utils.safestring import mark_safe


class IdeviceForm(forms.ModelForm):

    def render_edit(self):
        return self.as_p()

    def render_preview(self):
        return self._render_view("preview")

    def render_export(self):
        return self._render_view("export")

    def _render_view(self, purpose):
        '''Decouples field rendering from the purpose'''
        html = []
        renderer_name = "render_%s" % purpose
        for name, field_object in list(self.fields.items()):
            html.append(self._render_field(name, field_object, renderer_name))
        return mark_safe("\n".join(html))

    def _render_field(self, name, field, renderer_name):
        try:
            renderer = getattr(field.widget, renderer_name)
            return renderer(self.initial[name])
        except AttributeError as e:
            return ""

    @property
    def js_modules(self):
        modules = []
        for field in list(self.fields.values()):
            if hasattr(field.widget, "js_modules"):
                    modules += field.widget.js_modules
        return modules

class IdeviceFormFactory(object):
    def __init__(self, model, fields, form_class=IdeviceForm, widgets={},
                 media=None):

        self.model = model
        self.fields = fields
        self.widgets = widgets
        self.form = form_class
        self.media = media

        class NewIdeviceForm(self.form):

            class Meta:
                model = self.model
                if self.fields:
                    fields = self.fields
                exclude = ("parent_node", "edit")
                if self.widgets:
                    widgets = self.widgets
                if self.media is not None:
                    css = self.media._css
                    js = self.media._js

        self.form_class = NewIdeviceForm

    def __call__(self, *args, **kwargs):

        return self.form_class(*args, **kwargs)
