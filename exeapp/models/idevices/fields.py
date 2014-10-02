from django.db.models import TextField, CharField

from exeapp.views.blocks.widgets import FreeTextWidget, URLWidget, \
    ClozeWidget, \
    FeedbackWidget, MultiChoiceOptionWidget


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


class MultiChoiceOptionField(TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = MultiChoiceOptionWidget
        return super(MultiChoiceOptionField, self).formfield(**kwargs)
