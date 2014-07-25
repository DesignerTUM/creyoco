from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from exeapp.views.blocks.genericblock import  GenericBlock
from django.template.defaultfilters import unordered_list


class TOCBlock(GenericBlock):
    preview_template = "exe/idevices/toc/preview.html"
    view_template = "exe/idevices/toc/view.html"
    edit_template = "exe/idevices/toc/edit.html"

    def renderPreview(self):
        content = mark_safe(self.populate_toc(export_url=False))
        return render_to_string(self.preview_template, locals())

    def renderView(self):
        content = mark_safe(self.populate_toc(export_url=True))
        return render_to_string(self.view_template, locals())

    def renderEdit(self):
        return render_to_string(self.edit_template, {"idevice": self.idevice})

    def populate_toc(self, export_url):
        package = self.idevice.parent_node.package
        toc_list = [self._generate_item(package.root, export_url)]
        if package.root.children.exists():
            toc_list.append(self._generate_toc_tree(package.root, export_url))
        return '<ul class="toc">%s</ul>' % unordered_list(toc_list)

    def _generate_toc_tree(self, node, export_url):
        list = []
        for child in node.children.all():
            list.append(self._generate_item(child, export_url))
            if child.children.exists():
                list.append(self._generate_toc_tree(child, export_url))

        return list

    def _generate_item(self, node, export_url):
        print(export_url)
        if export_url:
            node_url = node.unique_name() + ".html"
        else:
            node_url = node.url()
        return '<a href="%s">%s</a>' %\
                    (node_url, node.title)
