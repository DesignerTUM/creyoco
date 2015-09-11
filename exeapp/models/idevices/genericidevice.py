import sys
import re

from django.db.models.fields import TextField
from bs4 import BeautifulSoup
from django.conf import settings

from exeapp.models.idevices.idevice import Idevice


if sys.version_info >= (3,):
    from urllib.request import unquote
else:
    from urllib import unquote


class GenericIdevice(Idevice):
    def _get_text_fields(self):
        return (getattr(self, field.attname)
                for field in self._meta.concrete_fields if
                isinstance(field, TextField))

    def _resources(self):
        user = self.parent_node.package.user
        media_url = user.profile.media_url
        resource_list = set()
        for field in self._get_text_fields():
            soup = BeautifulSoup(field)
            imgs = soup.findAll("img")
            for img in imgs:
                if not img['src'].startswith("data:image"):
                    resource_list.add(
                        unquote(img['src'].replace(media_url, "")))
            for link in soup.findAll("a"):
                if link.has_key("href") and link['href'].startswith(media_url):
                    resource_list.add(
                        unquote(link['href'].replace(media_url, "")))
            objs = soup.findAll("object")
            for obj in objs:
                # check if it is a full url
                obj_path = obj['data'].replace(
                    settings.STATIC_URL, settings.STATIC_ROOT + "/"
                )
                if obj_path.startswith("http"):
                    obj_path = "/" + "/".join(obj_path.split("/")[3:])
                resource_list.add(unquote(obj_path))
                flashvars = unquote(unquote(obj.findAll(
                    "param",
                    attrs={"name": "flashvars"})[0]['value']))
                for var in flashvars.split("&"):
                    name, _, value = var.partition("=")
                    if name == "url":
                        value.replace(media_url, "")
                        resource_list.add(unquote(value.replace(media_url, "")))
                        break
            videos = soup.findAll("video")
            for video in videos:
                video_sources = video.findAll("source")
                for video_source in video_sources:
                    if video_source['src'].startswith(media_url):
                        resource_list.add(
                            unquote(video_source['src'].replace(media_url, ""))
                        )
        return resource_list

    @property
    def link_list(self):
        parent = self.parent_node
        link_list = []
        for field in self._get_text_fields():
            link_list += (("%s::%s" % (parent.title, anchor), "%s.html#%s" % \
                           (parent.unique_name(), anchor)) \
                          for anchor in
                          re.findall('<a.*?name=[\"\'](.*?)[\"\']>',
                                     field))

        return link_list

    def __unicode__(self):
        return "%s: %s" % (self.__class__.__name__, self.pk)

    class Meta:
        app_label = "exeapp"
        proxy = True

