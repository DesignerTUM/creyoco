from django.forms.models import BaseInlineFormSet, inlineformset_factory
from exeapp.models.idevices.multiplechoiceidevice import MultipleChoiceQuestion,\
    MultipleChoiceOption, MultipleChoiceIdevice
from exeapp.views.blocks.formsetblock import BaseFormsetBlock
from django.forms.formsets import DELETION_FIELD_NAME



OptionsFormSet = inlineformset_factory(MultipleChoiceQuestion,
                                       MultipleChoiceOption,
                                       extra=1)

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
        nested =  OptionsFormSet(data=data, 
                                 instance=instance, 
                                 prefix="OPTION_%s" % pk_value)
        form.nested = nested
        
    def is_valid(self):
        result = super(BaseBuildingFormset, self).is_valid()
 
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
 
    def save_all(self, commit=True):
        """Save all formsets and along with their nested formsets."""
 
        # Save without committing (so self.saved_forms is populated)
        # -- We need self.saved_forms so we can go back and access
        #    the nested formsets
        objects = self.save(commit=False)
 
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
        
class MultipleChoiceBlock(BaseFormsetBlock):
    
    def __init__(self, *args, **kwargs):
        super(BaseFormsetBlock, self).__init__(*args, **kwargs)
        self.model = MultipleChoiceQuestion
        self.order = None
        self.BlockFormset = inlineformset_factory(self.idevice.__class__,
                                                  self.model,
                                                  formset=BaseQuestionFormSet)
        
        edit_template = "exe/idevices/multiplechoice/edit.html"