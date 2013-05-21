from exeapp.models.idevices.genericidevice import GenericIdevice
from django.utils.translation import ugettext_lazy as _
from django.db import models
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices import fields


class ObjectivesIdevice(GenericIdevice):

    name = _("Objectives")
    title = models.CharField(max_length=100, default=name)
    author = _("University of Auckland")
    purpose = _("""Objectives describe the expected outcomes of the learning "
    "and should define what the learners will be able to do when they have "
    "completed the learning tasks.""")
    emphasis = Idevice.SOMEEMPHASIS
    content = fields.RichTextField(blank=True, default="",
                  help_text=
                    _("Type the learning objectives for this resource."))
    group = Idevice.DIDACTICS

    class Meta:
        app_label = "exeapp"
