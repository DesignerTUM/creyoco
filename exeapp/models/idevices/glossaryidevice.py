from django.db import models
from django.utils.translation import ugettext_lazy as _
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices import fields

class GlossaryIdeviceManager(models.Manager):
    def create(self, *args, **kwargs):
        idevice = GlossaryIdevice(*args, **kwargs)
        idevice.save()
        GlossaryTerm.objects.create(title="", definition="", idevice=idevice)
        return idevice

class GlossaryIdevice(Idevice):

    name = _("Glossary")
    title = models.CharField(max_length=100, default=name)
    author = _("Technical University Munich")
    purpose = _("Adds a alphabethicaly sorted glossary")
    emphasis = Idevice.SOMEEMPHASIS
    group    = Idevice.CONTENT
    icon = "icon_summary.gif"

    objects = GlossaryIdeviceManager()

    def add_child(self):
        GlossaryTerm.objects.create(idevice=self)

    class Meta:
        app_label = "exeapp"


class GlossaryTerm(models.Model):

    title = fields.RichTextField(max_length=100, blank=True, default="",
                             help_text=_("Enter term you want to describe"))
    definition = fields.RichTextField(blank=True, default="",
                                 help_text=_("Enter defintion of the term"))
    idevice = models.ForeignKey("GlossaryIdevice", related_name="terms")

    class Meta:
        app_label = "exeapp"
