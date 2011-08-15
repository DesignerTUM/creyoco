from filebrowser.fields import FileBrowseWidget
from exeapp.views.blocks.ideviceform import IdeviceForm,\
    IdeviceFormFactory
from exeapp.views.blocks.genericblock import GenericBlock


class AppletBlock(GenericBlock):
    
    use_common_content = True
    content_template = "exe/idevices/applet/content.html"