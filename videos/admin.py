from django.contrib import admin
from django import forms
from .models import Video, Source, Chapter
from incuna.utils import find

class BaseSourceFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super(BaseSourceFormSet, self).clean()

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on it's own
            return

        if not find(lambda form: getattr(form, 'cleaned_data', None), self.forms):
            raise forms.ValidationError, 'Please specify at least one %s' % (self.model._meta.verbose_name)

class ChapterInline(admin.TabularInline):
    fields = ('title','timecode', 'preview')
    model = Chapter
    extra = 1

class SourceInline(admin.TabularInline):
    extra = 1
    fields = ('file', 'type')
    model = Source
    formset = BaseSourceFormSet

class VideoAdmin(admin.ModelAdmin):    
    inlines = [SourceInline, ChapterInline]
    list_display = ['title', 'preview', 'created', 'recorded']
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Video, VideoAdmin)


