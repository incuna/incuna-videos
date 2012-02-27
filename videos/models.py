import datetime
from django.conf import settings
from django.contrib import admin
from django.db import models
from incuna.db.models import AutoSlugField 
from django import forms
from django.utils.translation import ugettext_lazy as _

from settingsjs.signals import collect_settings
from django.dispatch import receiver

from incuna.utils.timesince import timesince
from incuna.utils import find
from incuna.utils.extensions import ExtensionsMixin


class VideoManager(models.Manager):
    def latest(self, limit=getattr(settings, 'VIDEOS_LATEST_LIMIT',3)):
        return self.get_query_set()[:limit]

class Video(models.Model, ExtensionsMixin):
    """
    Extendible video model.
    """
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=127,populate_from="title", editable=True, blank=True, unique=True,
                         help_text='This will be automatically generated from the title, and is used as the video\'s website address', )
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
        return timesince(datetime.time(0, 0, 0), self.length)

    @classmethod
    def register_extension(cls, register_fn):
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


class BaseSourceFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super(BaseSourceFormSet, self).clean()

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on it's own
            return

        if not find(lambda form: getattr(form, 'cleaned_data', None), self.forms):
            raise forms.ValidationError, 'Please specify at least one %s' % (self.model._meta.verbose_name)

class SourceInline(admin.TabularInline):
    extra = 1
    fields = ('file', 'type')
    model = Source
    formset = BaseSourceFormSet

class VideoAdmin(admin.ModelAdmin):
    inlines = [SourceInline,]
    list_display = ['title', 'preview', 'created', 'recorded']
    search_fields = ['title',]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [('', {
                    'fields': ['title', 'slug', 'preview', 'length', 'recorded',],
                })]

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


