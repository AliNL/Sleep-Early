#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import warnings
from io import BytesIO

import os
import wda
from PIL import Image

from atx.drivers import Display
from atx.drivers.mixin import DeviceMixin

__dir__ = os.path.dirname(os.path.abspath(__file__))


class IOSDevice(DeviceMixin):
    def __init__(self, device_url, bundle_id=None):
        DeviceMixin.__init__(self)
        self.__device_url = device_url
        self.__scale = None

        self._wda = wda.Client(device_url)
        self._session = None
        self._bundle_id = None

        if bundle_id:
            self.start_app(bundle_id)

    def start_app(self, bundle_id):
        self._bundle_id = bundle_id
        self._session = self._wda.session(bundle_id)
        return self._session

    @property
    def session(self):
        if self._session is None:
            self._session = self._wda.session()
        return self._session

    def stop_app(self):
        if self._session is None:
            return
        self._session.close()
        self._session = None
        self._bundle_id = None

    def __call__(self, *args, **kwargs):
        return self.session(*args, **kwargs)

    def status(self):
        """ Check if connection is ok """
        return self._wda.status()

    @property
    def display(self):
        """ Get screen width and height """
        w, h = self.session.window_size()
        return Display(w * self.scale, h * self.scale)

    @property
    def bundle_id(self):
        return self._bundle_id

    @property
    def scale(self):
        if self.__scale:
            return self.__scale
        wsize = self.session.window_size()
        # duplicate operation here. But do not want fix it now.
        self.__scale = min(self.screenshot().size) / min(wsize)
        # self.__scale = min(self.__screensize) / min(wsize)
        return self.__scale

    @property
    def rotation(self):
        """Rotation of device
        Returns:
            int (0-3)
        """
        rs = dict(PORTRAIT=0, LANDSCAPE=1, UIA_DEVICE_ORIENTATION_LANDSCAPERIGHT=3)
        return rs.get(self.session.orientation, 0)

    def type(self, text):
        """Type text
        Args:
            text(string): input text
        """
        self.session.send_keys(text)

    def click(self, x, y):
        """Simulate click operation
        Args:
            x, y(int): position
        """
        rx, ry = x / self.scale, y / self.scale
        self.session.tap(rx, ry)

    def swipe(self, x1, y1, x2, y2, duration=0.5):
        scale = self.scale
        x1, y1, x2, y2 = x1 / scale, y1 / scale, x2 / scale, y2 / scale
        self.session.swipe(x1, y1, x2, y2, duration)

    def home(self):
        """ Return to homescreen """
        return self._wda.home()

    def _take_screenshot(self):
        """Take a screenshot, also called by Mixin
        Args:
            - filename(string): file name to save

        Returns:
            PIL Image object
        """
        raw_png = self._wda.screenshot()
        img = Image.open(BytesIO(raw_png))
        return img

    def dump_view(self):
        """Dump page XML, Note, this is a test method"""
        warnings.warn("deprecated, use source() instead", DeprecationWarning)
        return self._wda.source()

    def source(self):
        """
        Dump page XML
        """
        return self._wda.source()
