from django.contrib import admin
from videos.module.chapters.models import Chapter

class ChapterInline(admin.TabularInline):
    fields = ('title','timecode', 'preview')
    model = Chapter
    extra = 1

def register(cls, admin_cls):
    if admin_cls:
        admin_cls.inlines = getattr(admin_cls, 'inlines', ()) + (ChapterInline, )

