from ..models import Video


Video.register_extensions(
    'videos.extensions.chapters',
    'videos.extensions.speakers',
    'videos.extensions.subtitle',
)
