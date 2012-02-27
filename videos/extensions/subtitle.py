from django.db import models

def register(cls, admin_cls):
    cls.add_to_class('sub_title', models.CharField(max_length=255, null=True, blank=True))

    if admin_cls:
        admin_cls.search_fields = list(admin_cls.search_fields) + ['sub_title',]
        if admin_cls.fieldsets:
            admin_cls.fieldsets[0][1]['fields'].insert(1, 'sub_title')


