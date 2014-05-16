import datetime

import factory

from .. import models
from videos.tests.factories import VideoFactory


class ChapterFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Chapter
    video = factory.SubFactory(VideoFactory)
    title = factory.Sequence(lambda i: 'Video {}'.format(i))
    timecode = datetime.time(minute=5)
