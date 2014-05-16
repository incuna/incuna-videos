import factory

from .. import models


class SpeakerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Speaker
