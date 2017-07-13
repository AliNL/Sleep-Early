# coding: utf-8

from __future__ import absolute_import

import collections
import re

import six

from atx import imutils
from atx import strutils

FindPoint = collections.namedtuple('FindPoint', ['pos', 'confidence', 'method', 'matched'])
Display = collections.namedtuple('Display', ['width', 'height'])

__boundstuple = collections.namedtuple('Bounds', ['left', 'top', 'right', 'bottom'])


class Bounds(__boundstuple):
    def __init__(self, *args, **kwargs):
        super(Bounds).__init__(*args, **kwargs)
        self._area = None

    def is_inside(self, x, y):
        v = self
        return v.left < x < v.right and v.top < y < v.bottom

    @property
    def area(self):
        if not self._area:
            v = self
            self._area = (v.right - v.left) * (v.bottom - v.top)
        return self._area

    @property
    def center(self):
        v = self
        return (v.left + v.right) / 2, (v.top + v.bottom) / 2

    def __mul__(self, mul):
        return Bounds(*(int(v * mul) for v in self))


class ImageCrop(object):
    def __init__(self, src, bound):
        self.src = src
        l, t, w, h = bound
        self.bound = Bounds(l, t, l + w, t + h)


class Pattern(object):
    def __init__(self, name, image=None, offset=None, rsl=None, resolution=None, th=None, threshold=None):
        if isinstance(name, ImageCrop):
            self.name_ = name.src
            self._bound = name.bound
        else:
            self.name_ = name
            self._bound = None

        self.image_ = image  # if image is None, it will delay to pattern_open function
        self._offset = offset
        self._resolution = rsl or resolution
        self._threshold = th or threshold
        if isinstance(image, six.string_types):
            self.name_ = image

        # search format name.1080x1920.png
        if self._resolution is None:
            m = re.search(r'\.(\d+)x(\d+)\.', self.name_)
            if m:
                (w, h) = sorted(map(int, (m.group(1), m.group(2))))
                # TODO(ssx): gcd(w, h), make sure the biggest < 20
                self._resolution = (w, h)

        if self._offset is None:
            m = re.search(r'\.([LRTB])(\d+)([LRTB])(\d+)\.', self.name_)
            if m:
                offx, offy = 0, 0
                for i in (1, 3):
                    flag, number = m.group(i), int(m.group(i + 1))
                    if flag in ('L', 'R'):
                        offx = number / 100.0 * (1 if flag == 'R' else -1)
                    if flag in ('T', 'B'):
                        offy = number / 100.0 * (1 if flag == 'B' else -1)
                self._offset = (offx, offy)

    def __str__(self):
        return 'Pattern(name: {}, offset: {})'.format(strutils.encode(self.name_), self.offset)

    def save(self, path):
        """ save image to path """
        import cv2
        cv2.imwrite(path, self.image_)

    @property
    def image(self):
        if self._bound is None:
            return self.image_
        else:
            return imutils.crop(self.image_, *self._bound)

    @property
    def offset(self):
        return self._offset

    @property
    def resolution(self):
        return self._resolution

    @property
    def threshold(self):
        return self._threshold
