from exeapp.models.idevices.idevice import Idevice

from exeapp.models.idevices.freetextidevice import FreeTextIdevice
from exeapp.models.idevices.activityidevice import ActivityIdevice
from exeapp.models.idevices.glossaryidevice import GlossaryIdevice
from exeapp.models.idevices.pdfidevice import PDFIdevice
from exeapp.models.idevices.readingactidevice import ReadingActivityIdevice
from exeapp.models.idevices.reflectionidevice import ReflectionIdevice
from exeapp.models.idevices.tocidevice import TOCIdevice
from exeapp.models.idevices.wikiidevice import WikipediaIdevice
from exeapp.models.idevices.objectivesidevice import ObjectivesIdevice
from exeapp.models.idevices.preknowledgeidevice import PreknowledgeIdevice
from exeapp.models.idevices.commentidevice import CommentIdevice
from exeapp.models.idevices.feedbackidevice import FeedbackIdevice
from exeapp.models.idevices.rssidevice import RSSIdevice
from exeapp.models.idevices.externalurlidevice import ExternalURLIdevice
from exeapp.models.idevices.appletidevice import AppletIdevice
from exeapp.models.idevices.clozeidevice import ClozeIdevice

idevice_list = [FreeTextIdevice,
            ActivityIdevice,
            GlossaryIdevice,
            ReadingActivityIdevice,
            ReflectionIdevice,
            TOCIdevice,
            WikipediaIdevice,
            PDFIdevice,
            ObjectivesIdevice,
            PreknowledgeIdevice,
            CommentIdevice,
            FeedbackIdevice,
            RSSIdevice,
            ExternalURLIdevice,
            AppletIdevice,
            ClozeIdevice,
            ]

__all__ = ['Idevice', 'idevice_list'] +\
                    [idevice.__name__ for idevice in idevice_list]
