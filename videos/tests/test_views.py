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
    def setUp(self):
        self.video = factories.VideoFactory.create()
        self.source = factories.SourceFactory.create(video=self.video)
        self.chapter = ChapterFactory.create(video=self.video)
        self.speaker = SpeakerFactory.create()
        self.video.speakers.add(self.speaker)

    def test_get_detail(self):
        view = views.VideoDetail.as_view()
        response = view(self.create_request(auth=False), slug=self.video.slug)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'], self.video)

        rendered_content = response.render().content.decode()

        self.assertIn(self.video.title, rendered_content)
        self.assertIn(self.source.get_absolute_url(), rendered_content)
        self.assertIn(self.source.get_type_display(), rendered_content)
        self.assertIn('href="#{}"'.format(self.chapter.seconds), rendered_content)
        self.assertIn(self.speaker.name, rendered_content)

    def test_get_content_data(self):
        view = views.VideoDetail()
        view.object = self.video
        context_data = view.get_context_data()
        expected = {
            'video': self.video,
            'view': view,
            'object': self.video,
            'sources': [self.source],
            'chapters': [self.chapter],
            'speakers': [self.speaker],
        }
        self.assertCountEqual(context_data, expected)


class TestVideoListLatest(RequestTestCase):
    def test_get_list(self):
        view = views.VideoListLatest.as_view()
        with mock.patch('videos.models.Video.objects.latest') as latest_method:
            response = view(self.create_request(auth=False))

        self.assertEqual(response.status_code, 200)
        latest_method.assert_called_with()
        self.assertEqual(response.context_data['object_list'], latest_method())
