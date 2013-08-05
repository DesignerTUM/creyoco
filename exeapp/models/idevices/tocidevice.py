from exeapp.models.idevices.genericidevice import GenericIdevice
from django.utils.translation import ugettext_lazy as _
from exeapp.models.idevices.idevice import Idevice
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import unordered_list
from exeapp.models.idevices import fields

class TOCIdevice(GenericIdevice):
    name = _("Table Of Content")
    title = name


    emphasis = Idevice.SOMEEMPHASIS
    group = Idevice.CONTENT
    content = fields.RichTextField(blank=True, default="")
    author = _("Technical University Munich")
    icon = "icon_inter.gif"
    edit_message = _("The content of this iDevice is automatically generated"
                    "should not be edited directly.")

    class Meta:
        app_label = "exeapp"
