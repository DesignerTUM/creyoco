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


class MultiChoiceOptionIdevice(models.Model):
    option = fields.MultiChoiceOptionField(
        blank=True, default="",
        help_text=_("An answer option for the multiple choice question. Check"
                    " the 'right answer' checkmark to mark the right option")
    )
    right_answer = models.BooleanField(default=False)
    idevice = models.ForeignKey("MultiChoiceIdevice", related_name="options")

    class Meta:
        app_label = "exeapp"
