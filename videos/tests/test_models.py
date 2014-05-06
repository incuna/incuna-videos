from django.test import TestCase

from .factories import VideoFactory
from .. import models


class TestVideo(TestCase):
    def test_fields(self):
        expected_fields = (
            'id',

            'title',
            'slug',
            'preview',
            'length',
            'recorded',
            'created',

            # Incoming
            'source',  # TODO: set a verbose name.
        )

        fields = models.Video._meta.get_all_field_names()
        self.assertCountEqual(fields, expected_fields)


class TestVideoManager(TestCase):
    def test_latest(self):
        """The default behaviour of 'Video.objects.latest()'"""
        VideoFactory.create_batch(4)
        latest = models.Video.objects.latest()
        self.assertIs(latest.count(), 3)  # 3 is the default

    def test_latest_none(self):
        """'Latest videos' when no Videos exist"""
        latest = models.Video.objects.latest()
        self.assertFalse(latest.exists())

    def test_latest_2(self):
        """An exact number of 'Video.objects.latest()'"""
        VideoFactory.create_batch(3)
        latest = models.Video.objects.latest(limit=2)
        self.assertIs(latest.count(), 2)

    def test_latest_setting(self):
        """Default setting of 'Video.objects.latest()'"""
        VideoFactory.create_batch(2)
        with self.settings(VIDEOS_LATEST_LIMIT=1):
            latest = models.Video.objects.latest()
        self.assertIs(latest.count(), 1)

class TestSource(TestCase):
    def test_fields(self):
        expected_fields = (
            'id',

            'video',
            'file',
            'type',
        )

        fields = models.Source._meta.get_all_field_names()
        self.assertCountEqual(fields, expected_fields)
