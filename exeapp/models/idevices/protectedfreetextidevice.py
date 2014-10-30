from datetime import datetime
import itertools
from exeapp.models.idevices import fields
from django.utils.translation import ugettext_lazy as _
from exeapp.models.idevices import Idevice
from django.db import models
from exeapp.models.idevices.genericidevice import GenericIdevice


class ProtectedFreeTextIdevice(GenericIdevice):
    group = Idevice.CONTENT
    name = _("Protected Free Text")
    title = _("Protected Free Text")

    password = models.CharField(max_length=20, blank=True, default="",
                        help_text=_("Input password to encrypt content"))

    purpose = _("""The majority of a learning resource will be
establishing context, delivering instructions and providing general information.
This provides the framework within which the learning activities are built and
delivered.""")
    emphasis = Idevice.NOEMPHASIS
    content = fields.RichTextField(blank=True, default="")
    date_created = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        app_label = "exeapp"

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'id'
                                    and k != 'idevice_ptr_id'
                                    and k != 'parent_node_id'
                                    and k != 'date_created'
                                    and not k.startswith('_')
            }
        d['child_type'] = self.get_klass()
        return d

    def from_dict(self, dic):
        print(dic)
        self.edit = dic['edit']
        self.content = dic['content']
        self.password = dic['password']
        self.date_created = datetime.now()
        self.save()
        ProtectedFreeTextVersion.objects.create(idevice=self, content=self.content, date_created=self.date_created)
        return self

    def has_previous_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return False
        if ProtectedFreeTextVersion.objects.filter(idevice_id=self.id, date_created__lt=date).count():
            return True
        else:
            return False

    def has_later_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return False
        if ProtectedFreeTextVersion.objects.filter(idevice_id=self.id, date_created__gt=date).count():
            return True
        else:
            return False

    def get_previous_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return None
        f1 = ProtectedFreeTextVersion.objects.filter(idevice_id=self.id, date_created__lt=date).order_by('-date_created')
        if f1.count() > 0:
            return f1[0]
        else:
            return None

    def get_later_version(self, date=None):
        if date is None:
            date = self.date_created
            if date is None:
                return None
        f = ProtectedFreeTextVersion.objects.filter(idevice_id=self.id, date_created__gt=date).order_by('date_created')
        if f.count() > 0:
            return f[0]
        else:
            return None

    def get_current_version(self):
        f = ProtectedFreeTextVersion.objects.filter(idevice_id=self.id, date_created=self.date_created)
        if f.count() > 0:
            return f[0]
        else:
            return None

    def delete_unnecessary_version(self):
        ProtectedFreeTextVersion.objects.filter(idevice_id=self.id, date_created__gt=self.date_created).delete()

    def apply_changes(self, formdata, formsetdata=None):
        #check for first time. it is none at first
        if self.date_created:
            self.delete_unnecessary_version()
        #check for same old version saving again. avoid duplication during creating versions
        v = self.get_current_version()
        if v is None:
            self.date_created = datetime.now()
            ProtectedFreeTextVersion.objects.create(idevice=self, content=formdata['content'], date_created=self.date_created)
        elif self.content != v.content:
            self.date_created = datetime.now()
            ProtectedFreeTextVersion.objects.create(idevice=self, content=formdata['content'], date_created=self.date_created)
        self.edit = False



# ===========================================================================

class ProtectedFreeTextVersion(models.Model):
    idevice = models.ForeignKey("ProtectedFreeTextIdevice", related_name="versions")
    content = fields.RichTextField(blank=True, default="")
    date_created = models.DateTimeField(default=datetime.now())

    class Meta:
        app_label = "exeapp"

