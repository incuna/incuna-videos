from feincms.models import create_base_model

from ..content import VideoContent
from ..models import Video


Video.register_extensions(
    'videos.extensions.captions',
    'videos.extensions.chapters',
    'videos.extensions.speakers',
    'videos.extensions.sub_heading',
)


class DummyPage(create_base_model()):
    """A fake class for holding content"""


class DummyArticle(create_base_model()):
    """Another fake class for holding content.

    Used to demonstrate the effects of assigning one ContentType to two models.
    """


DummyPage.register_regions(('main', 'Main content area'))
DummyPage.create_content_type(VideoContent, TYPE_CHOICES=(
    ('block', 'Block'),
))


DummyArticle.register_regions(('main', 'Main content area'))
DummyArticle.create_content_type(VideoContent, TYPE_CHOICES=(
    ('block', 'Block'),
))
