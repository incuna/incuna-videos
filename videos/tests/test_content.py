from django.test import TestCase
from incuna_test_utils.compat import Python2CountEqualMixin

from . import factories
from .models import DummyPage
from ..content import VideoContent


class CarouselContentTest(Python2CountEqualMixin, TestCase):
    model = DummyPage.content_type_for(VideoContent)

    def test_get_context(self):
        content = self.model(region='main')
        content.video = factories.VideoFactory.create()
        content.kwargs = {'request': 'dummy'}

        context = content.get_context_data()

        expected = {
            'type': 'block',  # Default set in 'models.py' when registered
            'video': content.video,
            'request': content.kwargs['request'],
        }
        self.assertCountEqual(context, expected)

    def test_get_template_names(self):
        content = self.model(region='main')
        expected = [
            'content/videocontent/main/block.html',
            'content/videocontent/main/default.html',
            'content/videocontent/block.html',
            'content/videocontent/default.html',
        ]
        self.assertCountEqual(content.get_template_names(), expected)
