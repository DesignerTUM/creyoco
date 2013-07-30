from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from exeapp.models.idevices.idevice import Idevice

class AppletIdevice(Idevice):


    name = _("Java Applet iDevice")
    title = name
    author = _("TU Munich")
    purpose = _('''Import java applets and display them
    Requires Java plugin.''')
    #pdf_file = models.CharField(max_length=100, blank=True, default="")
    java_file = FileBrowseField(_("Java Applet"), max_length=100,
                               directory="pdf/", extensions=['.class'],
                               blank=True, null=True)

    group = Idevice.MEDIA
    emphasis = Idevice.NOEMPHASIS

    @property
    def codebase(self):
        return self.java_file.url.replace(self.java_file.filename, "")

    def _resources(self):
        user = self.parent_node.package.user.username
        return set([self.java_file.path_relative_directory.replace("%s/" % user,
                                                                 "")])

    class Meta:
        app_label = "exeapp"
