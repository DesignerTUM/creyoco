from django.db import models
from exeapp.views.blocks.widgets import *

class RichTextField(models.TextField):
    
    def formfield(self, **kwargs):
        kwargs["widget"] = FreeTextWidget
        return super(RichTextField, self).formfield(**kwargs)
    
    def get_naked_code(self):
        '''Returns the content without <p> tags at the beginning and
        the end'''
        return self[3:-4]
    
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
    


