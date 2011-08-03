from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from incuna.db.models import AutoSlugField 
#from feincms.module.medialibrary.models import MediaFileBase

VIDEO_TYPES = getattr(settings, 
                      'VIDEO_TYPE', 
                      (
                          ('video/mp4; codecs="avc1.42E01E, mp4a.40.2"', 'mp4'),
                          ('video/webm; codecs="vp8, vorbis"', 'webm'),
                          ('video/ogg; codecs="theora, vorbis"', 'ogg'),
                      ),
                     )

class Video(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=127,populate_from="title", editable=True, blank=True, unique=True,
                         help_text='This will be automatically generated from the title, and is used as the video\'s website address', )
    preview = models.FileField(max_length=255, upload_to='videos/preview', null=True, blank=True, help_text=_('Preview image for this video.'))
    recorded = models.DateField(blank=True, null=True)
    created = models.DateTimeField(editable=False, default=datetime.now)

    def __unicode__(self):
        return self.title

class Chapter(models.Model):
    video = models.ForeignKey(Video)
    title = models.CharField(max_length=255)
    timecode = models.TimeField(help_text='hh:mm:ss')
    preview = models.ImageField(upload_to='videos/chapter/', null=True, blank=True, help_text=_('Preview image for this chapter.'))

    class Meta:
        ordering = ('timecode',)

    def __unicode__(self):
        return self.title

    @property
    def seconds(self):
        return self.timecode.hour*3600+self.timecode.minute*60+self.timecode.second



class Source(models.Model):
    video = models.ForeignKey(Video)
    file = models.FileField(upload_to='videos/%Y/%m/')
    type = models.CharField(max_length=255, choices=VIDEO_TYPES)

    def __unicode__(self):
        return u'%s %s' % (self.video.title, self.get_type_display())

