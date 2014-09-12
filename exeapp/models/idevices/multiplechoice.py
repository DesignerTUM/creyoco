#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices import fields


class MultiChoiceIdeviceManager(models.Manager):
    def create(self, *args, **kwargs):
        idevice = MultiChoiceIdevice(*args, **kwargs)
        idevice.save()
        MultiChoiceOptionIdevice.objects.create(idevice=idevice)
        return idevice


class MultiChoiceIdevice(Idevice):
    name = _("Multiple Choice")
    title = models.CharField(max_length=100, default=name)
    author = _("Technische Univesität München")
    purpose = _("""Create a multiple choice questionary to review the
    learned material""")
    emphasis = Idevice.SOMEEMPHASIS
    group = Idevice.TEST
    icon = "icon_question.gif"
    question = fields.RichTextField(
        blank=True,
        default="",
        help_text=_("""Create a multiple choice questionary to review the
    learned material. Click "Add option" to add more answer options""")
    )

    objects = MultiChoiceIdeviceManager()

    def add_child(self):
        MultiChoiceOptionIdevice.objects.create(idevice=self)

    class Meta:
        app_label = "exeapp"

    def submit_answers(self, data):
        chosen_option = MultiChoiceOptionIdevice.objects.get(pk=data['option'])
        assert chosen_option.idevice == self
        return chosen_option.right_answer

    def is_multioptional(self):
        """
        Returns true, if the question has more than one correct option
        """
        return self.options.filter(right_answer=True).count() > 1

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'id'
                                    and k != 'idevice_ptr_id'
                                    and k != 'parent_node_id'
                                    and not k.startswith('_')
            }
        d['child_type'] = self.get_klass()
        d['answers'] = []
        for answer in self.options.all():
            d['answers'].append(answer.to_dict())
        return d

    def from_dict(self, dic):
        print(dic)
        self.question = dic['question']
        self.edit = dic['edit']
        #clear blank answer created by default for this question in the manager
        MultiChoiceOptionIdevice.objects.filter(idevice=self).delete()
        for answer in dic['answers']:
            MultiChoiceOptionIdevice.objects.create(idevice=self,
                                                    option=answer['option'],
                                                    right_answer=answer['right_answer']
                                                    )
        self.save()
        return self


class MultiChoiceOptionIdevice(models.Model):
    option = fields.MultiChoiceOptionField(
        blank=True, default="",
        help_text=_("An answer option for the multiple choice question. Check"
                    " the 'right answer' checkmark to mark the right option")
    )
    right_answer = models.BooleanField(default=False)
    idevice = models.ForeignKey("MultiChoiceIdevice", related_name="options")

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'idevice_id'
                                    and k != 'id'
                                    and not k.startswith('_')
            }
        return d

    class Meta:
        app_label = "exeapp"
