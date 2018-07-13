from django.core.files import File
from fileinput import FileInput
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseField
from exeapp.models.idevices.idevice import Idevice
from exeapp.utils.path import Path
from django.conf import settings
import os

class PDFIdevice(Idevice):


    name = _("Pdf iDevice")
    title = name #models.CharField(max_length=100, default=name)
    author = _("Technical University Munich")
    purpose = _('''Import local pdf and display them.
    Requires Acrobat Reader plugin.''')
    #pdf_file = models.CharField(max_length=100, blank=True, default="")
    pdf_file = FileBrowseField("PDF", max_length=100,extensions=['.pdf'],
                               blank=True, null=True,
                               )
    modified_pdf_file = models.FilePathField(blank=True, null=True, editable=False)

    #height = models.PositiveIntegerField()
    page_list = models.CharField(max_length=50, blank=True, default="",
                        help_text=_("Input coma-separated pages or page ranges "
                                    "to import. For example: 1,2,3-8. Leave "
                                    "empty to import all pages"))
    formfield_overrides = {
        FileBrowseField: {'widget': FileInput},
    }
    group = Idevice.CONTENT
    emphasis = Idevice.NOEMPHASIS

    def to_dict(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k != 'id'
                                            and k != 'idevice_ptr_id'
                                            and k != 'parent_node_id'
                                            and k != 'pdf_file'
                                            and not k.startswith('_')
            }
        d['pdf_file_location'] = self.pdf_file.name if self.pdf_file else ""
        d['child_type'] = self.get_klass()
        return d

    def from_dict(self, dic):
        print(dic)
        self.edit = dic['edit']
        self.page_list = dic['page_list']
        self.modified_pdf_file = dic['modified_pdf_file']

        try:
            self.pdf_file = FileObject(dic['pdf_file_location'])
        except FileNotFoundError as E:
            print(E)
        self.save()
        return self

    def _resources(self):
        resource_list = set()
        if self.modified_pdf_file:
            resource_list.add(os.path.basename(self.modified_pdf_file))
        if self.pdf_file:
            resource_list.add(os.path.basename(self.pdf_file.path))
        return resource_list


    class Meta:
        app_label = "exeapp"
