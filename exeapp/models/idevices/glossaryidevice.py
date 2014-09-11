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
    group = Idevice.CONTENT
    icon = "icon_summary.gif"

    objects = GlossaryIdeviceManager()

    def add_child(self):
        GlossaryTerm.objects.create(idevice=self)

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'id'
                                    and k != 'idevice_ptr_id'
                                    and k != 'parent_node_id'
                                    and not k.startswith('_')
            }
        d['child_type'] = self.get_klass()
        d['terms'] = []
        for term in self.terms.all():
            d['terms'].append(term.to_dict())
        return d

    def from_dict(self, dic):
        print(dic)
        self.title = dic['title']
        self.edit = dic['edit']
        #clear blank answer created by default for this question in the manager
        GlossaryTerm.objects.filter(idevice=self).delete()
        for term in dic['terms']:
            GlossaryTerm.objects.create(idevice=self,
                                        title=term['title'],
                                        definition=term['definition']
                                        )
        self.save()
        return self

    class Meta:
        app_label = "exeapp"


class GlossaryTerm(models.Model):
    title = fields.RichTextField(max_length=100, blank=True, default="",
                                 help_text=_("Enter term you want to describe"))
    definition = fields.RichTextField(blank=True, default="",
                                      help_text=_(
                                          "Enter definition of the term"))
    idevice = models.ForeignKey("GlossaryIdevice", related_name="terms")

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'idevice_id'
                                    and k != 'id'
                                    and not k.startswith('_')
            }
        return d

    class Meta:
        app_label = "exeapp"
