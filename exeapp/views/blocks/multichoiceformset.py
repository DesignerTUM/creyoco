from exeapp.views.blocks.formsetblock import BaseFormsetBlock
from exeapp.views.blocks.ideviceform import IdeviceForm


class MultiChoiceFormsetBlock(BaseFormsetBlock):
    preview_template = "exe/idevices/mutlichoiceformset/preview.html"
    view_template = "exe/idevices/mutlichoiceformset/export.html"

    submit_action = "Submit"

    def process(self, action, data):
        if action == self.submit_action:
            right = self.idevice.submit_answers(data)
            html = self.renderPreview()
            html += "<p>{}</p>".format("right" if right else "wrong!")
            return html
        else:
            return super(MultiChoiceFormsetBlock, self).process(action, data)

    def _render_view(self, template, form=None, formset=None):
        self.BlockFormset.form.Meta.multioptional\
            =  self.idevice.is_multioptional()
        return super(MultiChoiceFormsetBlock, self)\
            ._render_view(template, form, formset)


class MultiChoiceForm(IdeviceForm):

    def _render_field(self, name, field, renderer_name):
        try:
            renderer = getattr(field.widget, renderer_name)
        except AttributeError:
            return ""
        else:
            field.widget.attrs['option_id'] = self.instance.pk
            field.widget.attrs['right'] = self.instance.right_answer
            field.widget.attrs['multioptional'] = self.Meta.multioptional
            field.widget.attrs['feedback'] = self.instance.feedback
            if name == "feedback": # don't render feedback
                return ''
            return renderer(self.initial[name])
