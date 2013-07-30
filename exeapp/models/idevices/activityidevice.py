from django.db import models
from django.utils.translation import ugettext_lazy as _
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices.genericidevice import GenericIdevice
from exeapp.models.idevices import fields


class ActivityIdevice(GenericIdevice):
    group = Idevice.CONTENT
    name = _("Activity")
    title = models.CharField(max_length=100, default=name)
    author = _("University of Auckland")
    purpose = _("""An activity can be defined as a task or set of tasks a
learner must complete. Provide a clear statement of the task and consider
any conditions that may help or hinder the learner in the performance of
the task.""")
    icon = "icon_activity.gif"
    emphasis = Idevice.SOMEEMPHASIS
    content = fields.RichTextField(blank=True, default="",
                                   help_text=_("Describe the tasks the "
                                                "learners should complete."))

    class Meta:
        app_label = "exeapp"
