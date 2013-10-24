$(function() {
    initVideo();
});
// initialise (load) flowplayer and add a preview image if the container has one.
jQuery.fn.sumHeight = function() {
    // sum the heights of the "selected" items.
    return _.reduce(this.map(function () {
        return $(this).height();
    }), function(memo, num){
        return memo + num;
    }, 0);
};

function initVideo(content) {
    content = content || $('body');
    var fpconfig = Setting.get('videos-fpconfig');

    content.find('.video-content').each(function() {
        var videocontent = $(this);
        var video = videocontent.find('video');
        var chapters = videocontent.find('.chapters');

        // Add flowplayer
        if ('application/x-shockwave-flash' in navigator.mimeTypes) {
            player = video.find('a:first').attr({'class': 'video'}).replaceAll(video).flowplayer(
                fpconfig.path, fpconfig).flowplayer(0);
            if (player) {
                player.awsrtmp();
            }

            // TODO make this a plugin
            var chapter_links = chapters.find('li a');
            if (chapter_links.length) {
                    // find the first non image clip
                    var clip = _(player.getPlaylist()).detect(function(c) {
                        return !('type' in c) || c.type != 'image';
                    });
                    var startAtIndex = clip && clip.index || 0;


                // Chapters seek
                chapter_links.click(function() {
                    $(this).closest('ul').find('.selected').removeClass('selected');
                    var href = $(this).addClass('selected').attr('href');
                    if (href.lastIndexOf('#')>-1) {
                        href = href.substr(href.lastIndexOf('#')+1);
                    }

                    player.startAt(parseInt(href, 10), startAtIndex);

                    return false;
                    });

                if (location.hash) {
                    chapter_links.filter('[href$='+location.hash+']:first').click();
                }

                // Chapter scroll
                (function () {
                    var max_height = chapters.height(),
                        ul_height = chapters.find('ul').height();

                    var cuepoints = chapter_links.map(function () {
                        var href = $(this).attr('href');
                        if (href.lastIndexOf('#')>-1) {
                            href = href.substr(href.lastIndexOf('#')+1);
                        }
                        return {
                            'time': parseInt(href, 10)*1000,
                            'id': $(this).attr('id')
                        };
                    });

                    player.onCuepoint(_.toArray(cuepoints), function(clip, cuepoint) {
                        //Add the selected class to the current chapter
                        chapter_links.removeClass('selected').filter('#'+cuepoint.id).addClass('selected');
                        chapters.trigger('seekTo', chapters.find("li").filter(':has(a.selected)').prevAll('li').length);
                    });

                    if (ul_height > max_height) {
                        // navigation buttons
                        var prev = $('<a>').addClass('navigation prev').html('<span>Previous</span>').css('visibility', 'hidden').click(function () {
                                chapters.trigger('prev');
                            }).insertBefore(chapters);
                        var next = $('<a>').addClass('navigation next').html('<span>Next</span>').click(function () {
                                chapters.trigger('next');
                            }).insertAfter(chapters);
                        var items = chapters.find('li');
                        var index = 0;
                        var overlap = ul_height - max_height;
                        var max_index = items.length - 1;

                        // calculate the (max) index necessary to (just) reveal the last item.
                        while (items.slice(0, max_index).sumHeight() > overlap) {
                            max_index -= 1;
                        }
                        max_index += 1;
                        chapters.bind('seekTo', function(event, i) {
                            index = Math.max(0, Math.min(i, max_index));
                            var top_offset = items.slice(0, index).sumHeight();
                            chapters.find('ul').animate({'top': -1*top_offset});

                            // sensitise the next / prev links
                            if (index > 0) {
                                prev.css('visibility', 'visible');
                            } else {
                                prev.css('visibility', 'hidden');
                            }

                            if (index < max_index) {
                                next.css('visibility', 'visible');
                            } else {
                                next.css('visibility', 'hidden');
                            }
                        });

                        chapters.bind('next', function(event) {
                            $(this).trigger('seekTo', index+1);
                        });
                        chapters.bind('prev', function(event) {
                            $(this).trigger('seekTo', index-1);
                        });
                    }
                })();
            }
        }
    });
}
