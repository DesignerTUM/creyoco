from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.http import QueryDict
from exeapp.models.idevices.multiplechoiceidevice import MultipleChoiceQuestion,\
    MultipleChoiceOption, MultipleChoiceIdevice
from exeapp.views.blocks.formsetblock import BaseFormsetBlock
from django.forms.formsets import DELETION_FIELD_NAME
from exeapp.views.blocks.ideviceform import IdeviceForm
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string



OptionsFormSet = inlineformset_factory(MultipleChoiceQuestion,
                                       MultipleChoiceOption,
                                       extra=0)

class BaseQuestionFormSet(BaseInlineFormSet):
    
    def add_fields(self, form, index):
        super(BaseQuestionFormSet, self).add_fields(form, index)
        
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance = None
            pk_value = hash(form.prefix)
        if self.data:
            data = self.data
        else:
            data = None
        
        nested = OptionsFormSet(data=data, 
                                 instance=instance, 
                                 prefix="OPTION_%s" % pk_value)
        form.nested = nested
        
    def is_valid(self):
        result = super(BaseQuestionFormSet, self).is_valid()
 
        for form in self.forms:
            if hasattr(form, 'nested'):
                for n in form.nested:
                    # make sure each nested formset is valid as well
                    result = result and n.is_valid()
 
        return result

    def save_new(self, form, commit=True):
        """Saves and returns a new model instance for the given form."""
 
        instance = super(BaseQuestionFormSet, self).save_new(form, commit=commit)
 
        # update the form's instance reference
        form.instance = instance
 
        # update the instance reference on nested forms
        form.nested.instance = instance
 
            # iterate over the cleaned_data of the nested formset and update the foreignkey reference
        for cd in form.nested.cleaned_data:
            cd[form.nested.fk.name] = instance
 
        return instance
    
    def should_delete(self, form):
        """Convenience method for determining if the form's object will
        be deleted; cribbed from BaseModelFormSet.save_existing_objects."""
 
        if self.can_delete:
            raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
            should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
            return should_delete
 
        return False
 
    def save(self, commit=True):
        """Save all formsets and along with their nested formsets."""
 
        # Save without committing (so self.saved_forms is populated)
        # -- We need self.saved_forms so we can go back and access
        #    the nested formsets
        objects = super(BaseQuestionFormSet, self).save(commit=False)
 
        # Save each instance if commit=True
        if commit:
            for o in objects:
                o.save()
 
        # save many to many fields if needed
        if not commit:
            self.save_m2m()
 
        # save the nested formsets
        for form in set(self.initial_forms + self.saved_forms):
            if self.should_delete(form): continue
 
            form.nested.save(commit=commit)
            
    def as_p(self):
        forms = u" ".join([form.as_p() + form.nested.as_p() \
                            for form in self])
        return mark_safe(u'\n'.join([unicode(self.management_form), forms]))
        
class MultipleChoiceBlock(BaseFormsetBlock):
    model = MultipleChoiceQuestion
    formset = BaseQuestionFormSet
    fields = ("question",)
    
    preview_template = "exe/idevices/multiplechoice/preview.html"
    edit_template = "exe/idevices/multiplechoice/edit.html"
    
