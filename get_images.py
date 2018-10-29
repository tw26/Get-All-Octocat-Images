#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from requests_html import HTMLSession

OCTODEX_URL = 'https://octodex.github.com'

ROOT_PATH = os.path.abspath('.')
IMAGES_DIR_PATH = os.path.join(ROOT_PATH, 'images')
if not os.path.exists(IMAGES_DIR_PATH):
    os.mkdir(IMAGES_DIR_PATH)


class OctocatImage(object):
    def __init__(self, name, image_name, image_url):
        self.name = name
        self.image_name = image_name
        self.image_url = image_url

    def __repr__(self):
        return '<OctocatImage name = %s, image_name = %s, image_url = %s>' % (self.name, self.image_name, self.image_url)


class OctocatImagesDownloader(object):

    def __init__(self):
        self.images = []

    def download(self):
        session = HTMLSession()
        response = session.get(OCTODEX_URL)

        hrefs = response.html.find('a.preview-image')
        for href in hrefs:
            name = href.attrs['href'][1:]
            src = href.find('img', first=True).attrs['data-src']
            image_name = src.split('/')[-1]
            image_url = OCTODEX_URL + src
            self.images.append(OctocatImage(name, image_name, image_url))

        for i in range(len(self.images)):
            image = self.images[i]
            print('downloading & saving image %d: %s...' % (i + 1, image))
            image_path = self.get_image_path(image.image_name)
            if self.is_image_downloaded(image_path):
                continue
            response = requests.get(image.image_url)
            self.save_image(image.image_name, response.content)
        print('Successfully downloaded & saved %s image(s) at %s' % (len(self.images), IMAGES_DIR_PATH))

    def get_image_path(self, image_name):
        return os.path.join(IMAGES_DIR_PATH, image_name)

    def is_image_downloaded(self, image_path):
        return os.path.exists(image_path)

    def save_image(self, image_name, image_data):
        if (not image_name) or (not image_data):
            print('image name or image data is empty!')
            return

        image_path = self.get_image_path(image_name)
        if not self.is_image_downloaded(image_path):
            with open(image_path, 'wb') as f:
                f.write(image_data)


if __name__ == '__main__':
    OctocatImagesDownloader().download()
