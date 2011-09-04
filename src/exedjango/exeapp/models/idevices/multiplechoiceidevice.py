from exeapp.models.idevices.idevice import Idevice
from django.db import models
from exeapp.models.idevices import fields

class MCIdeviceManager(models.Manager):
    
    def create(self, *args, **kwargs):
        idevice = MultipleChoiceIdevice(*args, **kwargs)
        idevice.save()
        MultipleChoiceQuestion.objects.create(idevice=idevice)
        return idevice
        
    
    

class MultipleChoiceIdevice(Idevice):
    
    name = "Multiple Choise"
    author = "University of Auckland"
    purpose = """Although more often used in formal testing 
situations MCQs can be used as a testing tool to stimulate thought and  
discussion on topics students may feel a little reticent in responding to. 

When designing a MCQ test consider the following:
<ul>
<li> What learning outcomes are the questions testing</li>
<li>    What intellectual skills are being tested</li>
<li> What are the language skills of the audience</li>
<li> Gender and cultural issues</li>
<li> Avoid grammar language and question structures that might provide 
     clues</li>
</ul>
 """
    group = Idevice.TEST
    title = models.CharField(max_length=100, default=name)
    objects = MCIdeviceManager()
    
    class Meta:
        app_label = "exeapp"
        
class MCQuestionManager(models.Manager):
    
    def create(self, *args, **kwargs):
        
        question = MultipleChoiceQuestion(*args, **kwargs)
        question.save()
        MultipleChoiceOption.objects.create(question=question)
        return question


class MultipleChoiceQuestion(models.Model):
    
    question = fields.RichTextField(blank=True, default="")
    idevice = models.ForeignKey(MultipleChoiceIdevice, related_name="questions")
    objects = MCQuestionManager()

    class Meta:
        app_label = "exeapp"



class MultipleChoiceOption(models.Model):
    
    option = fields.RichTextField(blank=True, default="")
    question = models.ForeignKey(MultipleChoiceQuestion, related_name="options")
    right_answer = models.BooleanField()
    

    class Meta:
        app_label = "exeapp"
