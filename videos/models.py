import datetime

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from feincms.extensions import ExtensionsMixin
from settingsjs.signals import collect_settings


class VideoManager(models.Manager):
    def latest(self, limit=None):
        if limit is None:
            limit = getattr(settings, 'VIDEOS_LATEST_LIMIT', 3)
        return self.get_query_set()[:limit]


class Video(models.Model, ExtensionsMixin):
    """
    Extendible video model.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=127,
        editable=True,
        unique=True,
        help_text=(
            "This will be automatically generated from the title, and " +
            "is used as the video's website address"
        ),
    )
    preview = models.FileField(max_length=255, upload_to='videos/preview', null=True, blank=True, help_text=_('Preview image for this video.'))
    length = models.TimeField(blank=True, null=True, help_text='hh:mm:ss')
    recorded = models.DateField(blank=True, null=True)
    created = models.DateTimeField(editable=False, default=datetime.datetime.now)

    objects = VideoManager()

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.title

    @property
    def length_display(self):
        raise NotImplementedError('https://github.com/incuna/incuna-videos/issues/8')
        return timesince(datetime.time(0, 0, 0), self.length)

    @classmethod
    def register_extension(cls, register_fn):
        from .admin import VideoAdmin
        register_fn(cls, VideoAdmin)


class Source(models.Model):
    """
    Video source (inspired by the HTML5 <source> tag)
    """
    TYPE_CHOICES = getattr(settings,
                          'VIDEO_TYPE_CHOICES',
                          (
                              ('video/mp4; codecs="avc1.42E01E, mp4a.40.2"', 'mp4'),
                              ('video/webm; codecs="vp8, vorbis"', 'webm'),
                              ('video/ogg; codecs="theora, vorbis"', 'ogg'),
                          ),
                         )
    video = models.ForeignKey(Video)
    file = models.FileField(upload_to='videos/%Y/%m/')
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)

    def __unicode__(self):
        return u'%s %s' % (self.video.title, self.get_type_display())


# Add videos specific js settings
@receiver(collect_settings)
def videos_settingsjs(sender, jssettings=None, **kwargs):
    if jssettings is not None:
        jssettings['videos-fpconfig'] = {
            "path": settings.STATIC_URL+"videos/flash/flowplayer.commercial-3.1.5.swf",
            "clip": {"scaling": "orig", "autoPlay": True},
            "key": getattr(settings, 'FLOWPLAYER_KEY', "#@c231218f702f09ba2ed"),
            "plugins": {
                "controls": {
                    "url": settings.STATIC_URL+"videos/flash/flowplayer.controls-3.1.5.swf",
                    'autoHide': 'always',
                    "backgroundColor": "#000000",
                },
            },
        }

        if hasattr(settings, 'AWS_CLOUDFRONT_STREAMING_DOMAIN'):
            jssettings['videos-fpconfig']['plugins']['rtmp'] ={
                "url": settings.STATIC_URL+"videos/flash/flowplayer.rtmp-3.1.3.swf",
                "netConnectionUrl": "rtmp://%s/cfx/st" % settings.AWS_CLOUDFRONT_STREAMING_DOMAIN,
            }
