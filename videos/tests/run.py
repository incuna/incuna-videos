#! /usr/bin/env python3
"""From http://stackoverflow.com/a/12260597/400691"""
from optparse import make_option, OptionParser
import sys

from colour_runner.django_runner import ColourRunnerMixin
import django
from django.conf import settings
import dj_database_url


settings.configure(
    DATABASES={
        'default': dj_database_url.config(default='postgres://localhost/videos'),
    },
    DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
    INSTALLED_APPS=(
        'videos',

        # Put contenttypes before auth to work around test issue.
        # See: https://code.djangoproject.com/ticket/10827#comment:12
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.admin',
    ),
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
    ROOT_URLCONF='videos.tests.urls',
)

try:
    django.setup()
except AttributeError:
    pass

try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from discover_runner.runner import DiscoverRunner


class Runner(ColourRunnerMixin, DiscoverRunner):
    pass


option_list = (
    make_option(
        '-v', '--verbosity', action='store', dest='verbosity', default='1',
        type='choice', choices=['0', '1', '2', '3'],
        help=('Verbosity level; 0=minimal output, 1=normal output, ' +
              '2=verbose output, 3=very verbose output'),
    ),
)

parser = OptionParser(option_list=option_list)
options, args = parser.parse_args()

test_runner = Runner(verbosity=int(options.verbosity))
failures = test_runner.run_tests(args)
if failures:
    sys.exit(1)
