from django.db import models
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices import fields

class CaseStudyIdeviceManager(models.Manager):
    def create(self, *args, **kwargs):
        idevice = CaseStudyIdevice(*args, **kwargs)
        idevice.save()
        CaseActivity.objects.create(idevice=idevice)
        return idevice
    
class CaseStudyIdevice(Idevice):
    
    name = "Case Study"
    title = models.CharField(max_length=100, default=name)
    author = "Technical University Munich"
    purpose = """A case study is a device that provides learners 
with a simulation that has an educational basis. It takes a situation, generally 
based in reality, and asks learners to demonstrate or describe what action they 
would take to complete a task or resolve a situation. The case study allows 
learners apply their own knowledge and experience to completing the tasks 
assigned. when designing a case study consider the following:<ul> 
<li>    What educational points are conveyed in the story</li>
<li>    What preparation will the learners need to do prior to working on the 
case study</li>
<li>    Where the case study fits into the rest of the course</li>
<li>    How the learners will interact with the materials and each other e.g.
if run in a classroom situation can teams be setup to work on different aspects
of the case and if so how are ideas feed back to the class</li></ul>"""
    emphasis = Idevice.SOMEEMPHASIS
    group    = Idevice.TEST
    icon = "icon_casestudy.gif"
    story = fields.RichTextField(blank=True, default="",
                 help_text="""Create the case story. A good case is one 
that describes a controversy or sets the scene by describing the characters 
involved and the situation. It should also allow for some action to be taken 
in order to gain resolution of the situation.""")
    
    objects = CaseStudyIdeviceManager()
    
    def add_term(self):
        CaseActivity.objects.create(idevice=self)
    
    class Meta:
        app_label = "exeapp"
    

class CaseActivity(models.Model):
    
    activity = fields.RichTextField(blank=True, default="",
             help_text="Describe the activity tasks relevant to the case story provided. These could be in the form of questions or instructions for activity which may lead the learner to resolving a dilemma presented. ")
    feedback = fields.FeedbackField(blank=True, default="",
             help_text="Provide relevant feedback on the situation")
    idevice = models.ForeignKey("CaseStudyIdevice", related_name="terms")
    
    class Meta:
        app_label = "exeapp"
