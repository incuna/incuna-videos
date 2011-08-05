from django.conf.urls.defaults import *
from .models import Video

urlpatterns = patterns(
    'videos.views',
    url(r'^$', 'videos_list', {'queryset': Video.objects.latest}, name='videos_latest'),
    url(r'^all/$', 'videos_list', name='videos_all'),
    url(r'^(?P<slug>[a-z0-9_-]+).html$', 'videos_detail', name='videos_detail'),
)
