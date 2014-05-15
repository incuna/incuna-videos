from incuna_test_utils.testcases.request import RequestTestCase
import mock

from . import factories
from .. import views


class TestVideoList(RequestTestCase):
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

        view = views.VideoDetail.as_view()
        response = view(self.create_request(auth=False), slug=video.slug)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'], video)


class TestVideoListLatest(RequestTestCase):
    def test_get_list(self):
        view = views.VideoListLatest.as_view()
        with mock.patch('videos.models.Video.objects.latest') as latest_method:
            response = view(self.create_request(auth=False))

        self.assertEqual(response.status_code, 200)
        latest_method.assert_called_with()
        self.assertEqual(response.context_data['object_list'], latest_method())
