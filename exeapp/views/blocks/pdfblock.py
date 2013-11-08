from exeapp.views.blocks.genericblock import GenericBlock
from bs4 import BeautifulSoup


class PDFBlock(GenericBlock):

    use_common_content = True
    content_template = "exe/idevices/pdf/content.html"

    def renderView(self):
        soup = BeautifulSoup(super(PDFBlock, self).renderView())
        url = soup.findAll('object')[0]['data']
        soup.findAll('object')[0]['data'] = soup.findAll('object')[0]['data'].\
                                                split("/")[-1]
        return str(soup)
