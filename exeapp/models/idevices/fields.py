from django.db.models import TextField, CharField
from south.modelsinspector import add_introspection_rules

from exeapp.views.blocks.widgets import FreeTextWidget, URLWidget, \
    ClozeWidget, \
    FeedbackWidget


add_introspection_rules([],
    ["^exeapp\.models\.idevices\.fields\.RichTextField"])
add_introspection_rules([],
    ["^exeapp\.models\.idevices\.fields\.FeedbackField"])
add_introspection_rules([], ["^exeapp\.models\.idevices\.fields\.URLField"])
add_introspection_rules([],
    ["^exeapp\.models\.idevices\.fields\.ClozeTextField"])


class RichTextField(TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = FreeTextWidget
        return super(RichTextField, self).formfield(**kwargs)


class FeedbackField(TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = FeedbackWidget
        return super(FeedbackField, self).formfield(**kwargs)


class URLField(CharField):
    def formfield(self, **kwargs):
        kwargs["widget"] = URLWidget
        return super(URLField, self).formfield(**kwargs)


class ClozeTextField(TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = ClozeWidget
        return super(ClozeTextField, self).formfield(**kwargs)
