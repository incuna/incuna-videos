from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class VideoContent(models.Model):
    """Display a video in all its glorious formats"""
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
            'videos/content/%s/%s.html' % (self.region, self.type),
            'videos/content/%s/default.html' % self.region,
            'videos/content/%s.html' % self.type,
            'videos/content/default.html',
        ]

    def get_context_data(self, **kwargs):
        context = {
            'video': self.video,
            'type': self.type,
            'request': self.kwargs.get('request'),
            'sources': self.video.source_set.all(),
        }
        extensions = (
            ('chapters', 'chapter_set'),
            ('speakers', 'speakers'),
        )
        for key, manager_name in extensions:
            manager = getattr(self.video, manager_name, None)
            if manager:
                context.update({key: manager.all()})
        return context

    def render(self, **kwargs):
        self.kwargs = kwargs
        self.request = kwargs.get('request')
        templates = self.get_template_names()
        context = self.get_context_data()
        return render_to_string(templates, context)
