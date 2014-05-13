# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class FooCall(object):
    def __call__(self, a, b):
        print(a, b)


class FooNewInit(object):
    def __new__(cls, *args, **kwargs):
        print('FooNewInit.__new()__')
        return super(FooNewInit, cls).__new__(cls, *args)

    def __init__(self):
        print('FooNewInit.__init()__')


class FooSingleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(FooSingleton, cls).__new__(cls, *args)
        return cls._instance

    def __init__(self, a, b):
        self.a = a
        self.b = b


class FooSingletonNoInit(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(FooSingletonNoInit, cls).__new__(cls, *args)
        return cls._instance


class ChildFooSingletonNoInit(FooSingletonNoInit):
    def __init__(self, a, b):
        self.a = a
        self.b = b


if __name__ == '__main__':
    foo_call = FooCall()
    print('foo_call is callable(): {}'.format(callable(foo_call)))
    foo_call('python', '3')
    foo_new_init = FooNewInit()
    print("*************")
    singleton_1 = FooSingleton(1, 2)
    print('singleton_1.a: {}'.format(singleton_1.a))
    print('singleton_1.b: {}'.format(singleton_1.b))
    singleton_2 = FooSingleton(3, 4)
    print('singleton_1 is singleton_2: {}'.format(singleton_1 is singleton_2))
    print('singleton_1.a: {}'.format(singleton_1.a))
    print('singleton_1.b: {}'.format(singleton_1.b))
    print("*************")
    sni_1 = ChildFooSingletonNoInit(1, 2)
    print('sni_1.a: {}'.format(sni_1.a))
    print('sni_1.b: {}'.format(sni_1.b))
    sni_2 = ChildFooSingletonNoInit(3, 4)
    print('sni_1 is sni_2: {}'.format(sni_1 is sni_2))
    print('sni_1.a: {}'.format(sni_1.a))
    print('sni_1.b: {}'.format(sni_1.b))



