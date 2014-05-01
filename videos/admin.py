from django.contrib import admin
from .models import Video, VideoAdmin


admin.site.register(Video, VideoAdmin)
