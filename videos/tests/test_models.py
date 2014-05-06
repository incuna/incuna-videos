# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from incuna_test_utils.testcases.compat import Python2CountEqualMixin

from .factories import SourceFactory, VideoFactory
from .. import models
from ..compat import DJANGO_LT_17, string_type


def clean_fields(fields):
    """Remove fields ending in '_id' (on django < 1.7)"""
    def clean_id_field(name):
        return None if name.endswith('_id') and DJANGO_LT_17 else name
    return filter(clean_id_field, fields)


class TestVideo(Python2CountEqualMixin, TestCase):
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


class TestVideoUnicode(TestCase):
    def test_cast_to_unicode_string(self):
        expected = 'ツ'
        video = VideoFactory.build(title=expected)
        self.assertEqual(string_type(video), expected)


class TestSource(Python2CountEqualMixin, TestCase):
    def test_fields(self):
        expected_fields = (
            'id',

            'video',
            'video_id',
            'file',
            'type',
        )

        expected_fields = clean_fields(expected_fields)

        fields = models.Source._meta.get_all_field_names()
        self.assertCountEqual(fields, expected_fields)


class TestSourceUnicode(TestCase):
    def test_cast_to_unicode_string(self):
        video_title = 'ツ'
        source = SourceFactory.build(
            video__title=video_title,
            type=models.Source.TYPE_MP4,
        )
        expected = '{title} {type}'.format(title=video_title, type='mp4')
        self.assertEqual(string_type(source), expected)
