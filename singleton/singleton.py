# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Child(Singleton):
    pass
