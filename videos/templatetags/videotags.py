from django import template

register = template.Library()
@register.inclusion_tag('videos/_video.html')
def video(video):
    """
    Render the video.
    """
    
    return {'video': video,}

