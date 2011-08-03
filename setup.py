from setuptools import setup, find_packages

from videos import get_version
setup(
    name = "django-videos",
    packages = find_packages(),
    include_package_data=True,
    version = get_version(),
    description = "Generic extensible video content.",
    author = "Incuna Ltd",
    author_email = "admin@incuna.com",
    url = "http://incuna.com/",
)
