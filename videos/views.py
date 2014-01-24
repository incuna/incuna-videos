from django.views.generic import DetailView, ListView

from .models import Video


class VideoList(ListView):
    template_name = 'videos/list.html'
    model = Video


class VideoListLatest(VideoList):
    def get_queryset(self):
        return Video.objects.latest()


class VideoDetail(DetailView):
    template_name = 'videos/detail.html'
    model = Video
