from exeapp.views.blocks.genericblock import GenericBlock

class FreeTextBlock(GenericBlock):
    #use_common_content = True
    edit_template = "exe/idevices/freetext/edit.html"
    preview_template = "exe/idevices/generic/preview.html"
    def process(self, action, data):
        if action == "Earlier Version":
            has_version = self.idevice.has_previous_version(date=self.idevice.date_created)
            if has_version:
                older_version = self.idevice.get_previous_version(date=self.idevice.date_created)
                self.idevice.content = older_version.content
                self.idevice.date_created = older_version.date_created
                self.idevice.save()
            return self.render()
        elif action == "Later Version":
            has_version = self.idevice.has_later_version(date=self.idevice.date_created)
            if has_version:
                older_version = self.idevice.get_later_version(date=self.idevice.date_created)
                self.idevice.content = older_version.content
                self.idevice.date_created = older_version.date_created
                self.idevice.save()
            return self.render()
        else:
            return super(FreeTextBlock, self).process(action, data)