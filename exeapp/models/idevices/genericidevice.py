import re
from urllib.request import unquote
from exeapp.models.idevices.idevice import Idevice
from django.db.models.fields import TextField
from bs4 import BeautifulSoup
from django.conf import settings


class GenericIdevice(Idevice):

    def _get_text_fields(self):
        return (getattr(self, field.attname) for field in self._meta._fields() if
                isinstance(field, TextField))

    def _resources(self):
        user = self.parent_node.package.user
        media_url = user.get_profile().media_url
        resource_list = set()
        for field in self._get_text_fields():
            soup = BeautifulSoup(field)
            imgs = soup.findAll("img")
            for img in imgs:
                resource_list.add(img['src'].replace(media_url, ""))
            objs = soup.findAll("object")
            for obj in objs:
                resource_list.add(obj['data'].replace(
                    settings.STATIC_URL, settings.STATIC_ROOT + "/"))
                flashvars = unquote(unquote(obj.findAll(
                    "param",
                    attrs={"name": "flashvars"})[0]['value']))
                for var in flashvars.split("&"):
                    name, _, value = var.partition("=")
                    if name == "url":
                        value.replace(media_url, "")
                        resource_list.add(value.replace(media_url, ""))
                        break
        return resource_list

    @property
    def link_list(self):
        parent = self.parent_node
        link_list = []
        for field in self._get_text_fields():
            link_list += (("%s::%s" % (parent.title, anchor), "%s.html#%s" %\
                                          (parent.unique_name(), anchor)) \
                   for anchor in re.findall('<a.*?name=[\"\'](.*?)[\"\']>',
                                                         field))


        return link_list

    def __unicode__(self):
        return "%s: %s" % (self.__class__.__name__, self.pk)

    class Meta:
        app_label = "exeapp"
        proxy = True

