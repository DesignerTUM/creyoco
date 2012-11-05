from django.db import models
from filebrowser.fields import FileBrowseField
from exeapp.models.idevices.idevice import Idevice

class AppletIdevice(Idevice):
    

    name = "Java Applet iDevice"
    title = name 
    author = "TU Munich"
    purpose = '''Import java applets and display them
    Requires Java plugin.'''
    #pdf_file = models.CharField(max_length=100, blank=True, default="")
    java_file = FileBrowseField("Java Applet", max_length=100,
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
