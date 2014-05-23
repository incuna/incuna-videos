# Changelog for `incuna-videos`

## v2.0.0

* Remove requirement of legacy closed source `django-incuna` library.
* Preliminary python 3 support
* Tests!
* Remove `video` and `video_hours_count` tempate tags.
* Remove flowplayer and all javascript.
* OPEN SOURCE! WOO! (BSD 2-Clause License)
* Replace `sorl-thumbnail` with `django-imagekit`.
* Make "Chapter.seconds" return an int
* Add `VideoContent`
* Set `related_name` on `Source.video` and `Chapter.video`

**Known issues:**
* `Video.length_display` Is totally disabled -- this will get fixed in a later version
    (See https://github.com/incuna/incuna-videos/issues/8)

## v1.0

**Backwards incompatible: may break project extensions.**

* Use feincms.extensions.ExtensionsMixin rather than incuna.utils.extensions.ExtensionsMixin
  From FeinCMS v1.7 extensions sub class feincms.extensions.ExtensionsMixin.
  Support for register(cls, admin_cls)-style functions is removed in FeinCMS v1.9.
* Convert all extension to sub class feincms.extensions.ExtensionsMixin.

## v0.7

* Convert views to use generic class based views.
* Update templates to use new `{% url %}` format, this breaks compatibility with Django < 1.5.

## v0.6.2

* Flowplayer will now only use mp4 or m4v sources.

## v0.6.1

* Tweaked video template and updated README.

## v0.6

* Added subtitle extension.

## v0.5.2

* Tweaked js.

## v0.5.1

* Fixed cyclic models import causing admin to not display chapters.

## v0.5

* Round the video hours up if above 30 minutes and use a decimal instead of a time in the template.

## v0.4.1

* Strip the template right down so projects can override it.

## v0.4

## v0.3.4

* Add an inclusion tag to get total number of video hours.

## v0.3.3

* Added install_requires django-settingsjs.
* Moved js settings to django-settingsjs.

## v0.3.2

* Added media.
* Fixed chapters links.

## v0.3.1

* Template tweak.

## v0.3

* Added List and latest views.

## v0.2

* Tweaked video markup.

## v0.1

* Changed package name.
* Added install_requires django-incuna>=2.0.
* Refactored to use ExtensionsMixin.
* Fixed urls.
* Created as new.