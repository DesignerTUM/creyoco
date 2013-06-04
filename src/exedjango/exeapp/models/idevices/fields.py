from django.db import models
from exeapp.views.blocks.widgets import *
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^exeapp\.models\.idevices\.fields\.RichTextField"])
add_introspection_rules([], ["^exeapp\.models\.idevices\.fields\.FeedbackField"])
add_introspection_rules([], ["^exeapp\.models\.idevices\.fields\.URLField"])
add_introspection_rules([], ["^exeapp\.models\.idevices\.fields\.ClozeTextField"])

class RichTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = FreeTextWidget
        return super(RichTextField, self).formfield(**kwargs)


class FeedbackField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = FeedbackWidget
        return super(FeedbackField, self).formfield(**kwargs)


class URLField(models.CharField):
    def formfield(self, **kwargs):
        kwargs["widget"] = URLWidget
        return super(URLField, self).formfield(**kwargs)


class ClozeTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = ClozeWidget
        return super(ClozeTextField, self).formfield(**kwargs)

