from django.db import models
from django.utils.translation import ugettext_lazy as _

from videos.models import Video

class Chapter(models.Model):
    """
    Video section.
    """
    video = models.ForeignKey(Video)
    title = models.CharField(max_length=255)
    timecode = models.TimeField(help_text='hh:mm:ss')
    preview = models.ImageField(upload_to='videos/chapter/', null=True, blank=True, help_text=_('Preview image for this chapter.'))

    class Meta:
        app_label = 'videos'
        ordering = ('timecode',)

    def __unicode__(self):
        return self.title

    @property
    def seconds(self):
        return self.timecode.hour*3600+self.timecode.minute*60+self.timecode.second

