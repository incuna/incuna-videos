import factory

from .. import models


class SourceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Source

    video = factory.SubFactory('videos.tests.factories.VideoFactory')
    type = models.Source.TYPE_MP4  # An arbitrary default for the factory


class VideoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Video

    title = factory.Sequence(lambda i: 'Video {}'.format(i))
    slug = factory.Sequence(lambda i: 'video-{}'.format(i))
