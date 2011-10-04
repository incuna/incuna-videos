from datetime import datetime, timedelta, time

from django import template

from models import Video

register = template.Library()
@register.inclusion_tag('videos/_video.html')
def video(video):
    """
    Render the video.
    """
    return {'video': video,}

@register.inclusion_tag('videos/_video_hours_count.html')
def video_hours_count():
    total_time = timedelta()
    for video in Video.objects.all():
        total_time = total_time + timedelta(hours=video.length.hour, minutes=video.length.minute, seconds=video.length.second)
    return {'hours': (datetime.min + total_time).time()}

