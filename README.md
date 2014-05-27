# `incuna-videos` [![Build Status](https://travis-ci.org/incuna/incuna-videos.svg?branch=master)](https://travis-ci.org/incuna/incuna-videos) [![Coverage Status](https://img.shields.io/coveralls/incuna/incuna-videos.svg)](https://coveralls.io/r/incuna/incuna-videos?branch=master)

An extensible Django app, that can output a `<video>` tag with a number of sources. These are represented by a `Video` and `Source` model.

The concept (and some code) is borrowed from the [FeinCMS](https://github.com/feincms/feincms) `Page` model.

## Installation

To use the videos module add `videos` to your `INSTALLED_APPS`.

**Warning:** Before proceeding with `manage.py syncdb`, you may want to add some video extensions.


### Video extension modules

Extensions are a way to add often-used functionality the Video model.

To register extensions, call `Video.register_extensions` from a `models.py` file that will get imported at run-time:

    from videos.models import Video
    Video.register_extensions(
        'videos.extensions.chapters',
        'videos.extensions.speakers',
        'myapp.videoextensions',
    )

If the extension requires its own models (like the chapters and speakers extension) then the app containing the models will also need to be added to your INSTALLED_APPS. ie:

    INSTALLED_APPS += ['videos.module.chapters', ...]

### Custom extensions

You may be interested in the documentation for [FeinCMS extensions](http://feincms-django-cms.readthedocs.org/en/latest/extensions.html).
## FeinCMS Content

A `VideoContent` [FeinCMS content type](feincms-django-cms.readthedocs.org/en/latest/contenttypes.html) is available in `videos.content`

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

## Dependencies

* [FeinCMS](http://www.feincms.org/)

    This facilitates the extensions and content-types mechanisms.

* [django-imagekit](http://django-imagekit.readthedocs.org/en/latest/)

    This is used to scale the preview/cover image of the Video object.
