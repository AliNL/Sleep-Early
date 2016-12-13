#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import time

import wda
import subprocess32 as subprocess
from PIL import Image
from StringIO import StringIO

from atx.drivers.mixin import DeviceMixin, hook_wrap
from atx.drivers import Display
from atx import consts
from atx import ioskit

__dir__ = os.path.dirname(os.path.abspath(__file__))


class IOSDevice(DeviceMixin):
    def __init__(self, device_url, bundle_id=None):
        DeviceMixin.__init__(self)
        self.__device_url = device_url
        self.__display = None
        self.__scale = None

        self._wda = wda.Client(device_url)
        self._session = None
        self._bundle_id = None

        if bundle_id:
            self.start_app(bundle_id)

        # ioskit.Device.__init__(self, udid)

        # # xcodebuild -project  -scheme WebDriverAgentRunner -destination "id=1002c0174e481a651d71e3d9a89bd6f90d253446" test
        # # Test Case '-[UITestingUITests testRunner]' started.
        # xproj_dir = os.getenv('WEBDRIVERAGENT_DIR')
        # if not xproj_dir:
        #     raise RuntimeError("env-var WEBDRIVERAGENT_DIR need to be set")

        # proc = self._xcproc = subprocess.Popen(['/usr/bin/xcodebuild',
        #     '-project', 'WebDriverAgent.xcodeproj',
        #     '-scheme', 'WebDriverAgentRunner',
        #     '-destination', 'id='+self.udid, 'test'],
        #     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=xproj_dir, bufsize=1, universal_newlines=True)
        # for line in iter(proc.stdout.readline, b""):
        #     print 'STDOUT:', line.strip()
        #     if 'TEST FAILED' in line:
        #         raise RuntimeError("webdriver start test failed, maybe need to unlock the keychain, try\n" +
        #             '$ security unlock-keychain ~/Library/Keychains/login.keychain')
        #     elif "Successfully wrote Manifest cache" in line:
        #         print 'GOOD ^_^, wait 5s'
        #         time.sleep(5.0)
        #         break

    def start_app(self, bundle_id):
        """Start an application
        Args:
            - bundle_id: (string) apk bundle ID

        Returns:
            WDA session object
        """
        # if self._session is not None:
        #     self.stop_app()
        self._bundle_id = bundle_id
        self._session = self._wda.session(bundle_id)
        return self._session

    @property
    def session(self):
        if self._session is None:
            self._session = self._wda.session()
        return self._session

    def stop_app(self, *args):
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
        if not self.__display:
            self.screenshot()
        return self.__display

    @property
    def bundle_id(self):
        return self._bundle_id

    @property
    def scale(self):
        if self.__scale:
            return self.__scale
        wsize = self.session.window_size()
        self.__scale = min(self.display) / min(wsize)
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
        sx, sy = x, y
        if self.rotation == 1:
            x = self.display[0] - sy
            y = sx
        elif self.rotation == 2:
            x = sy
            y = self.display[1] - sx
        rx, ry = x/self.scale, y/self.scale
        self.session.tap(rx, ry)

    def swipe(self, x1, y1, x2, y2, duration=0.5):
        """Simulate swipe operation
        Args:
            x1, y1(int): from position
            x2, y2(int): to position
            duration(float): swipe duration, unit seconds
        """
        sx1, sy1, sx2, sy2 = x1, y1, x2, y2
        if self.rotation == 1:
            x1 = self.display[0] - sy1
            y1 = sx1
            x2 = self.display[0] - sy2
            y2 = sx2
        elif self.rotation == 2:
            x1 = sy1
            y1 = self.display[1] - sx1
            x2 = sy2
            y2 = self.display[1] - sx2

        scale = self.scale
        x1, y1, x2, y2 = x1/scale, y1/scale, x2/scale, y2/scale
        self.session.swipe(x1, y1, x2, y2, duration)

    def home(self):
        """ Return to homescreen """
        return self._wda.home()

    @hook_wrap(consts.EVENT_SCREENSHOT)
    def screenshot(self, filename=None):
        """Take a screenshot
        Args:
            - filename(string): file name to save

        Returns:
            PIL Image object
        """
        raw_png = self._wda.screenshot()
        img = Image.open(StringIO(raw_png))
        if filename:
            img.save(filename)
        if not self.__display:
            self.__display = Display(*sorted(img.size))
        return img
