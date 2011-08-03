from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from .models import Video

def videos_list(request, template="videos/list.html", queryset=None, extra_context=None):

    if queryset is None:
        queryset = Video.objects.all()


    context = RequestContext(request)

    context.update({
        'video_list': queryset,
    })
    print "videos_list", queryset

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context)


def videos_detail(request, slug, template="videos/detail.html", extra_context=None):

    video = get_object_or_404(Video, slug=slug)

    context = RequestContext(request)

    context.update({
        'video': video,
    })

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context)

