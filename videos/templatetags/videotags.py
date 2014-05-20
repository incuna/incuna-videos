from datetime import datetime, timedelta

from django import template

from videos.models import Video


register = template.Library()


@register.inclusion_tag('videos/_video_hours_count.html')
def video_hours_count():
    total_time = timedelta()
    for video in Video.objects.all():
        total_time = total_time + timedelta(hours=video.length.hour, minutes=video.length.minute, seconds=video.length.second)
    result = (datetime.min + total_time)
    if result.minute > 30:
        result = result + timedelta(hours=1)
    return {'hours': result.hour}
