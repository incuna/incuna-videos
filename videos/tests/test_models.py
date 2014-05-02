from django.test import TestCase

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
