from django.forms.models import modelformset_factory
from django.template.loader import render_to_string

from exeapp.utils.compat import with_metaclass
from exeapp.views.blocks.genericblock import GenericBlock
from exeapp.views.blocks.ideviceform import IdeviceFormFactory


def FormsetBlockMetaclassFactory(model, fields, media=None, base_form=None):
    class FormsetBlockMetaclass(type):
        def __new__(cls, name, bases, cls_dict):
            cls_dict.update({"formset_media": media})
            form_dict = {"model": model, "fields": fields}
            cls_dict.update(form_dict)
            if base_form is not None:
                form_dict['form_class'] = base_form
            cls_dict['form_class'] = IdeviceFormFactory(**form_dict).form_class
            return type.__new__(cls, name, bases, cls_dict)

    return FormsetBlockMetaclass


class BaseFormsetBlock(GenericBlock):
    def __init__(self, *args, **kwargs):
        super(BaseFormsetBlock, self).__init__(*args, **kwargs)

        self.BlockFormset = modelformset_factory(
            self.model, self.form_class,
            fields=self.fields,
            extra=0,
            can_delete=True,
        )

    edit_template = "exe/idevices/formsetblock/edit.html"
    preview_template = "exe/idevices/formsetblock/preview.html"
    view_template = "exe/idevices/formsetblock/export.html"
    add_action = "Add Item"
    remove_action = "Remove Selected Items"

    def process(self, action, data):
        if action == self.add_action:
            self.handle_apply_changes(data)
            self.idevice.edit = True
            self.idevice.add_child()
            return self.render()
        elif action == self.remove_action:
            self.handle_apply_changes(data)
            self.idevice.edit = True
            return self.render()
        elif action == "apply_changes":
            form, formset = self.handle_apply_changes(data)
            return self.render(form=form, formset=formset)
        else:
            return super(BaseFormsetBlock, self).process(action, data)

    def handle_apply_changes(self, data):
        form = self.BlockForm(data, instance=self.idevice)
        formset = self.BlockFormset(data)
        if formset.is_valid() and form.is_valid():
            form.save(commit=False)
            self.idevice.apply_changes(form.cleaned_data, formset.cleaned_data)
            formset.save()
        return form, formset

    @property
    def media(self):
        media = super(BaseFormsetBlock, self).media
        media += self.formset_media
        if not self.idevice.edit:
            media += self.BlockFormset().form().media
        return media

    @property
    def js_modules(self):
        modules = super(BaseFormsetBlock, self).js_modules
        if not self.idevice.edit:
            modules += self.BlockFormset().form().js_modules
        return modules


    def _render_view(self, template, form=None, formset=None):
        form = form or self.BlockForm(
            instance=self.idevice,
            auto_id="%s_field_" % self.idevice.id + "%s"
        )
        formset = formset or self.BlockFormset(queryset=self.model. \
            objects.filter(idevice=self.idevice))
        try:
            html = render_to_string(template, {"idevice": self.idevice,
                                               "form": form,
                                               "formset": formset,
                                               "self": self,
            })
        except Exception as e:
            print(e)
        else:
            return html


def FormsetBlockFactory(model, fields, media=None, base=BaseFormsetBlock,
                        base_form=None):
    metaclass = FormsetBlockMetaclassFactory(model, fields, media, base_form)

    class FormsetBlock(with_metaclass(metaclass, base)):
        pass

    return FormsetBlock
