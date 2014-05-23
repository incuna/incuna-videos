## Extensible videos for Django

This is an extensible videos app for Django, designed to provide a simple Video model that is extensible.

The concept (and some code) is borrowed from the FeinCMS (https://github.com/feincms/feincms) page model.

To use the videos module add `videos` to your `INSTALLED_APPS`.

Before proceeding with `manage.py syncdb`, you may want to add some video extensions.


### Video extension modules

Extensions are a way to add often-used functionality the Video model. The extensions are standard python modules with a register() method which will be called upon registering the extension. The register() method receives the Video class itself and the model admin class VideoAdmin as arguments.

To register extensions, call Video.register_extensions from a models.py file that will be processed anyway:

    from videos.models import Video
    Video.register_extensions(
        'videos.extensions.chapters',
        'videos.extensions.speakers',
        'myapp.videoextensions',
    )

If the extension requires it's own models (like the chapters and speakers extension) then the app containing the models will also need to be added to your INSTALLED_APPS.

### Createing extensions

To create an extension create a python module that defines a register function that accepts the Video class and the VideoAdmin class as arguments and modifies them as required.

Here is the **speakers** extension (`videos/extensions/speakers.py`):

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


A VideoContent FeinCMS content type is available in `videos.content`

Example usage: 

    from videos.content import VideoContent
    Page.create_content_type(
        VideoContent,
        TYPE_CHOICES=(
            ('block', _('block')),
            ('left', _('left')),
            ('right', _('right')),
        )
    )

### Dependencies

* [FeinCMS](http://www.feincms.org/)

    This facilitates the extensions mechanism.

* [django-imagekit](http://django-imagekit.readthedocs.org/en/latest/)

    This is used to scale the preview/cover image of the Video object.
