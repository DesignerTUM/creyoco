from django.db import models
from django.utils.translation import ugettext_lazy as _
from exeapp.models.idevices.idevice import Idevice
from exeapp.models.idevices.genericidevice import GenericIdevice
from exeapp.models.idevices import fields

class ClozeIdevice(GenericIdevice):

    group = Idevice.TEST
    name = _("Cloze")
    title = models.CharField(max_length=100, default=name)
    author = _("University of Auckland")
    purpose = _("""<p>Cloze exercises are texts or
                    sentences where students must fill in
                    missing words. They are often used for the
                    following purposes:</p>
                    <ol>
                    <li>To check knowledge of core course
                    concepts (this could be a pre-check,
                    formative exercise, or summative check).</li>
                    <li>To check reading comprehension.</li>
                    <li>To check vocabulary knowledge.</li>
                    <li>To check word formation and/or grammatical
                    competence. </li></ol>""")
    emphasis = Idevice.SOMEEMPHASIS
    icon = "icon_question.gif"
    description = fields.RichTextField(blank=True, default="",
                help_text=_("""Provide instruction on how the cloze activity should be
completed. Default text will be entered if there are no changes to this field.
"""))
    cloze_text = fields.ClozeTextField(blank=True, default="",
                help_text=_("""Enter the text for the cloze activity in to the cloze field
by either pasting text from another source or by typing text directly into the
field.To select words to hide, double click on the word to select it and
click on the underscore button in the toolbar."""))
    feedback = fields.FeedbackField(blank=True, default="",
                help_text=_("""Enter any feedback you wish to provide the learner
                with-in the feedback field. This field can be left blank."""))
    drag_n_drop = models.BooleanField(default=False)

    class Meta:
        app_label = "exeapp"

