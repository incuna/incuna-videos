import django


try:
    string_type = unicode
except NameError:
    string_type = str


DJANGO_LT_17 = django.VERSION < (1, 7)
