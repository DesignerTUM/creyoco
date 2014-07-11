from exeapp.views.blocks.genericblock import GenericBlock
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileWriter, PdfFileReader
from exeapp.utils.misc import pages_from_range
from exeapp.utils.path import Path
from django.conf import settings

class PDFBlock(GenericBlock):

    use_common_content = True
    content_template = "exe/idevices/pdf/content.html"


    def renderView(self):
        soup = BeautifulSoup(super(PDFBlock, self).renderView())
        url = soup.findAll('object')[0]['data']
        soup.findAll('object')[0]['data'] = soup.findAll('object')[0]['data'].\
                                                split("/")[-1]
        return str(soup)

    def renderPreview(self):
        """
        Returns an XHTML string for previewing this block
        """
        if self.idevice.page_list:
            print("\n\n######################\n")
            print("render preview ")
            filename = Path.joinpath(Path(settings.MEDIA_ROOT),Path.relpath(self.idevice.pdf_file.path))
            modified_filename = Path._get_namebase(filename) + "-modified-"+ str(self.idevice.id)+ Path._get_ext(filename)
            pages = pages_from_range(self.idevice.page_list)

            output = PdfFileWriter()
            input = PdfFileReader(open(filename, "rb"))
            for page in pages:
                output.addPage(input.getPage(page-1))
            with open(modified_filename,'wb') as output_pdf:
                output.write(output_pdf)
            self.idevice.modified_pdf_file = Path.joinpath(Path(self.idevice.parent_node.package.user.get_profile().media_url), Path.basename(modified_filename))


            print("\n\n######################\n")

        template = self.COMMON_PREVIEW if self.use_common_content else \
            self.preview_template
        return self._render_view(template)