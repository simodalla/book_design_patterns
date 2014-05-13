# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class HTTPConnection(object):
    def connect(self):
        print('http connection')


class FTPConnection(object):
    def connect(self):
        print('ftp connection')


class SimpleFactory(object):
    @staticmethod
    def build_connection(protocol):
        if protocol == 'http':
            return HTTPConnection()
        elif protocol == 'ftp':
            return FTPConnection()
        else:
            raise RuntimeError('Unknown protocol')


if __name__ == '__main__':
    protocol = raw_input('Which protocol to use (http or ftp): ')
    protocol = SimpleFactory.build_connection(protocol)
    protocol.connect()
