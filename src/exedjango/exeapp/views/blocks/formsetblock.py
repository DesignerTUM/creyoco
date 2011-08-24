from django import forms
from exeapp.views.blocks.genericblock import GenericBlock
from django.forms.models import modelformset_factory
from django.template.loader import render_to_string
from exeapp.views.blocks.ideviceform import IdeviceForm

def FormsetBlockMetaclassFactory(model, fields, form=None, order=None):
    class FormsetBlockMetaclass(type):
        def __new__(cls, name, bases, dict):
            dict.update({"model" : model,
                         "fields" :  fields,
                         "form" : form,
                         "order" : order})
            return type.__new__(cls, name, bases, dict)
    return FormsetBlockMetaclass

class BaseFormsetBlock(GenericBlock):
    
    def __init__(self, *args, **kwargs):
        super(BaseFormsetBlock, self).__init__(*args, **kwargs)
        
        class FormsetItemForm(self.form or IdeviceForm):
            pass
            
            class Meta:
                model = self.model
                fields = self.fields
                
        self.BlockFormset = modelformset_factory(
                                self.model, FormsetItemForm,
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
            self.idevice.add_term()
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
            self.idevice.apply_changes(form.cleaned_data)
            formset.save()
        return form, formset
    
    @property
    def media(self):
        media = super(BaseFormsetBlock, self).media
        if not self.idevice.edit:
            media += self.BlockFormset().form().view_media
        return media
    
    
    def _render_view(self, template, form=None, formset=None):
        form = form or self.BlockForm(instance=self.idevice)
        queryset = self.model.objects.filter(idevice=self.idevice)
        if self.order is not None:
            queryset = queryset.order_by(self.order)
        formset = formset or self.BlockFormset(queryset=queryset)
        try:
            html = render_to_string(template, {"idevice" : self.idevice,
                                           "form" : form,
                                           "formset" : formset,
                                           "self" : self,
                                           })
        except Exception, e:
            print e
        else:
            return html
        
def FormsetBlockFactory(model, fields, form=None, order=None):
    metaclass = FormsetBlockMetaclassFactory(model, fields, form, order)
    class FormsetBlock(BaseFormsetBlock):
        __metaclass__ = metaclass
        
    return FormsetBlock