'''
Created on Apr 18, 2011

@author: Alendit

Provides block_factory. Returns block object based on given idevice.
'''
from django import forms
from django.conf import settings
from exeapp.models.idevices.multiplechoice import MultiChoiceIdevice, \
    MultiChoiceOptionIdevice
from exeapp.models.idevices.protectedfreetextidevice import ProtectedFreeTextIdevice
from exeapp.views.blocks.clozetextblock import ClozeTextBlock
from exeapp.views.blocks.freetextblock import FreeTextBlock

from exeapp.views.blocks.genericblock import GenericBlock
from exeapp.models.idevices import FreeTextIdevice
from exeapp.models.idevices.activityidevice import ActivityIdevice
from exeapp.models.idevices.glossaryidevice import GlossaryIdevice
from exeapp.models.idevices.pdfidevice import PDFIdevice
from exeapp.views.blocks.multichoiceformset import MultiChoiceFormsetBlock, \
    MultiChoiceForm
from exeapp.views.blocks.pdfblock import PDFBlock
from exeapp.models.idevices.readingactidevice import ReadingActivityIdevice
from exeapp.models.idevices.reflectionidevice import ReflectionIdevice
from exeapp.models.idevices.tocidevice import TOCIdevice
from exeapp.models.idevices.wikiidevice import WikipediaIdevice
from exeapp.views.blocks.protectedfreetextblock import ProtectedFreeTextBlock
from exeapp.views.blocks.wikiblock import WikipediaBlock
from exeapp.models.idevices.objectivesidevice import ObjectivesIdevice
from exeapp.models import PreknowledgeIdevice
from exeapp.models import CommentIdevice
from exeapp.views.blocks.commentblock import CommentBlock
from exeapp.models import FeedbackIdevice
from exeapp.views.blocks.feedbackblock import FeedbackBlock
from exeapp.models import RSSIdevice
from exeapp.views.blocks.rssblock import RSSBlock
from exeapp.models import ExternalURLIdevice
from exeapp.views.blocks.externalurlblock import ExternalURLBlock
from exeapp.models import AppletIdevice
from exeapp.views.blocks.appletblock import AppletBlock
from exeapp.models import ClozeIdevice
from exeapp.views.blocks.formsetblock import FormsetBlockFactory
from exeapp.models import CaseStudyIdevice
from exeapp.models.idevices.casestudyidevice import CaseActivity
from exeapp.views.blocks.glossaryblock import GlossaryBlock
from exeapp.views.blocks.tocblock import TOCBlock

idevice_map = {
    FreeTextIdevice: FreeTextBlock,
    ProtectedFreeTextIdevice: ProtectedFreeTextBlock,
    ActivityIdevice: GenericBlock,
    GlossaryIdevice: GlossaryBlock,
    ReadingActivityIdevice: GenericBlock,
    ReflectionIdevice: GenericBlock,
    TOCIdevice: TOCBlock,
    WikipediaIdevice: WikipediaBlock,
    PDFIdevice: PDFBlock,
    ObjectivesIdevice: GenericBlock,
    PreknowledgeIdevice: GenericBlock,
    CommentIdevice: CommentBlock,
    FeedbackIdevice: FeedbackBlock,
    RSSIdevice: RSSBlock,
    ExternalURLIdevice: ExternalURLBlock,
    AppletIdevice: AppletBlock,
    ClozeIdevice: ClozeTextBlock,
    CaseStudyIdevice: FormsetBlockFactory(
        CaseActivity,
        ("activity", "feedback"),
    ),
    MultiChoiceIdevice: FormsetBlockFactory(
        MultiChoiceOptionIdevice,
        ("option", "right_answer"),
        forms.Media(
            js=['{}scripts/blocks/multichoice.js'.format(settings.STATIC_URL)],
            css={'all': ['{}css/blocks/multichoice.css' \
                             .format(settings.STATIC_URL)]},
        ),
        base=MultiChoiceFormsetBlock,
        base_form=MultiChoiceForm
    )
}

block_map = dict((v, k) for k, v in list(idevice_map.items()))


block_factory = lambda idevice: idevice_map[idevice.__class__](idevice)


def idevice_class_factory(block):
    if isinstance(block, type):
        return block_map[block]
    else:
        return block_map[block.__class__]

