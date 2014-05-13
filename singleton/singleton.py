# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Singleton(object):
    def __new__(cls):
        print(cls)
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Child(Singleton):
    pass


class Borg(object):
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Borg, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ == cls._shared_state
        return obj


class BorgChild(Borg):
    pass


