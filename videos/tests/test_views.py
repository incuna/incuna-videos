from incuna_test_utils.compat import Python2CountEqualMixin
from incuna_test_utils.testcases.request import RequestTestCase
import mock

from . import factories
from .. import views
from videos.module.chapters.tests.factories import ChapterFactory
from videos.module.speakers.tests.factories import SpeakerFactory


class TestVideoList(Python2CountEqualMixin, RequestTestCase):
    def test_get_empty_list(self):
        view = views.VideoList.as_view()
        response = view(self.create_request(auth=False))

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context_data['object_list'], [])

    def test_get_list(self):
        video = factories.VideoFactory.create()

        view = views.VideoList.as_view()
        response = view(self.create_request(auth=False))

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context_data['object_list'], [video])


class TestVideoDetail(RequestTestCase):
    def test_get_detail(self):
        video = factories.VideoFactory.create()
        source = factories.SourceFactory.create(video=video)
        chapter = ChapterFactory.create(video=video)
        speaker = SpeakerFactory.create()
        video.speakers.add(speaker)

        view = views.VideoDetail.as_view()
        response = view(self.create_request(auth=False), slug=video.slug)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'], video)

        rendered_content = response.render().content.decode()

        self.assertIn(video.title, rendered_content)
        self.assertIn(source.get_absolute_url(), rendered_content)
        self.assertIn(source.get_type_display(), rendered_content)
        self.assertIn('href="#{}"'.format(chapter.seconds), rendered_content)
        self.assertIn(speaker.name, rendered_content)


class TestVideoListLatest(RequestTestCase):
    def test_get_list(self):
        view = views.VideoListLatest.as_view()
        with mock.patch('videos.models.Video.objects.latest') as latest_method:
            response = view(self.create_request(auth=False))

        self.assertEqual(response.status_code, 200)
        latest_method.assert_called_with()
        self.assertEqual(response.context_data['object_list'], latest_method())
