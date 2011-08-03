from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('speakers', models.ManyToManyField('videos.Speaker', null=True, blank=True))

    if admin_cls:
        admin_cls.list_display_filter = getattr(admin_cls, 'list_display_filter', ()) + ('speakers', )
        admin_cls.filter_horizontal = getattr(admin_cls, 'filter_horizontal', ()) + ('speakers',)

        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Speakers'), {
                    'fields': ['speakers',],
                    'classes': ('collapse',),
                }))

