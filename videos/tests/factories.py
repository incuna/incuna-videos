import factory

from .. import models


class VideoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Video

    title = factory.Sequence(lambda i: 'Video {}'.format(i))
    slug = factory.Sequence(lambda i: 'video-{}'.format(i))
