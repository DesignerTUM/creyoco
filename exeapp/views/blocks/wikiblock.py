from exeapp.views.blocks.genericblock import GenericBlock


class WikipediaBlock(GenericBlock):

    def process(self, action, data):
        if action == "Load":
            self.idevice.load_article(data['article_name'])
            self.idevice.save()
            return self.render()
        else:
            return super(WikipediaBlock, self).process(action, data)
