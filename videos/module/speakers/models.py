from django.db import models
from incuna.db.models import AutoSlugField 

class Speaker(models.Model):
    """A person who features in a video"""
    name = models.CharField(max_length=127)
    slug = AutoSlugField(max_length=127,populate_from="name",
                         help_text='This will be automatically generated from the name, and is used as the speaker\'s website address', editable=True, blank=True, unique=True)

    class Meta:
        app_label = 'videos'

    def __unicode__(self):
        return self.name

