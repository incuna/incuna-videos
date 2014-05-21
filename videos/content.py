from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class VideoContent(models.Model):
    """Display a video in all it's glorious formats"""
    video = models.ForeignKey('videos.Video', verbose_name=_('video'))

    class Meta:
        abstract = True
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    @classmethod
    def initialize_type(cls, TYPE_CHOICES=None):
        if TYPE_CHOICES is None:
            msg = 'You have to set TYPE_CHOICES when creating a {}'
            raise ImproperlyConfigured(msg.format(cls.__name__))

        cls.add_to_class(
            'type',
            models.CharField(
                _('type'),
                max_length=255,
                choices=TYPE_CHOICES,
                default=TYPE_CHOICES[0][0],
            )
        )

    def get_template_names(self):
        return [
            'content/videocontent/%s/%s.html' % (self.region, self.position),
            'content/videocontent/%s/default.html' % self.region,
            'content/videocontent/%s.html' % self.position,
            'content/videocontent/default.html',
        ]

    def get_context_data(self, **kwargs):
        return {'content': self, 'request': self.kwargs.get('request')}

    def render(self, **kwargs):
        templates = self.get_template_names()
        context = self.get_context_data()
        return render_to_string(templates, context)
