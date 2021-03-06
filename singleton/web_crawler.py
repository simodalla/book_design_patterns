# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import re
import threading
import urllib
from urlparse import urlparse, urljoin

import httplib2
from BeautifulSoup import BeautifulSoup


parsed_root = None


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class ImageDownloaderThread(threading.Thread):
    """A thread for downloading images in parallel"""
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print('Starting thread {}'.format(self.name))
        download_images(self.name)
        print('Finished thread {}'.format(self.name))


def traverse_site(max_links=10):
    link_parser_singleton = Singleton()

    # While we have pages to parse in queue
    while link_parser_singleton.queue_to_parse:
        # If collected enough links to download images, return
        if len(link_parser_singleton.to_visit) == max_links:
            return
        url = link_parser_singleton.queue_to_parse.pop()

        http = httplib2.Http()
        try:
            status, response = http.request(url)
        except Exception as e:
            # raise e
            continue

        # Skip if not a web page
        if not status.get('content-type').startswith('text/html'):
            continue

        # Add the link to queue for downloading images
        link_parser_singleton.to_visit.add(url)
        print('Added {} to queue'.format(url))

        bs = BeautifulSoup(response)

        for link in BeautifulSoup.findAll(bs, 'a'):
            link_url = link.get('href')
            # <img> tag may not contain href attribute
            if not link_url:
                continue

            parsed = urlparse(link_url)

            # If link follows to external webpage, skip it
            if parsed.netloc and parsed.netloc != parsed_root.netloc:
                continue

            # Construct a fulll url from a link which can be relative
            link_url = (
                ((parsed.scheme or parsed_root.scheme) + '://' +
                (parsed.netloc or parsed_root.netloc) + parsed.path) or '')

            # If link was added previously, skip it
            if link_url in link_parser_singleton.to_visit:
                continue

            # Add a link tp further parsing
            link_parser_singleton.queue_to_parse = (
                [link_url] + link_parser_singleton.queue_to_parse)


def download_images(thread_name):
    singleton = Singleton()
    # While we have pages where we have noy download images
    while singleton.to_visit:
        url = singleton.to_visit.pop()

        http = httplib2.Http()
        print("{} starting downloading images from {}".format(
            thread_name, url))
        try:
            status, response = http.request(url)
        except Exception:
            continue
        bs = BeautifulSoup(response)

        # Find all <img> tags
        for image in BeautifulSoup.findAll(bs, 'img'):
            # Get image source url which can be absoluthe or relative
            src = image.get('src')
            # Construct a full url
            src = urljoin(url, src)

            basename = os.path.basename(src)
            if src not in singleton.downloaded:
                singleton.downloaded.add(src)
                print('Downloading {}'.format(src))
                # Download image to local filesystem
                urllib.urlretrieve(src, os.path.join('images', basename))

        print('{} finshed downloading images from {}'.format(thread_name,
                                                             url))


if __name__ == '__main__':
    root = 'https://www.python.org'
    parsed_root = urlparse(root)

    singleton = Singleton()
    singleton.queue_to_parse = [root]
    singleton.to_visit = set()
    singleton.downloaded = set()

    traverse_site()

    if not os.path.exists('images'):
        os.makedirs('images')

    thread1 = ImageDownloaderThread(1, "Thread-1", 1)
    thread2 = ImageDownloaderThread(2, "Thread-2", 2)

    thread1.start()
    thread2.start()




