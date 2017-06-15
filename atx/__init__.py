#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is to make mobile test more easily
"""

from __future__ import absolute_import

import os
import sys
import six

import pkg_resources
try:
    version = pkg_resources.get_distribution("atx").version
except pkg_resources.DistributionNotFound:
    version = 'unknown'

from atx.consts import *
from atx.errors import *
from atx.drivers import Pattern, Bounds, ImageCrop


def _connect_url(*args):
    if len(args) == 0:
        return os.getenv('ATX_CONNECT_URL')
    return args[0]


def _detect_platform(connect_url):
    if os.getenv('ATX_PLATFORM'):
        return os.getenv('ATX_PLATFORM')

    if not connect_url:  # None or ""
        return 'android'
    elif connect_url.startswith('http://'):  # WDA use http url as connect str
        return 'ios'
    else:
        return 'android'


def connect(*args, **kwargs):
    connect_url = _connect_url(*args)
    platform = kwargs.pop('platform', _detect_platform(connect_url))

    if platform == 'windows':
        from atx.drivers.windows import WindowsDevice
        return WindowsDevice(connect_url, **kwargs)
    elif platform == 'ios':
        from atx.drivers.ios_webdriveragent import IOSDevice
        return IOSDevice(connect_url, **kwargs)
    elif platform == 'webdriver':
        from atx.drivers.webdriver import WebDriver
        return WebDriver(connect_url)
    elif platform == 'dummy':
        from atx.drivers.dummy import DummyDevice
        return DummyDevice(connect_url, **kwargs)
    else:
        os.environ['JSONRPC_TIMEOUT'] = "60"  # default is 90s which is too long.
        from atx.drivers.android import AndroidDevice
        return AndroidDevice(connect_url, **kwargs)

# def _sig_handler(signum, frame):
#     print >>sys.stderr, 'Signal INT catched !!!'
#     sys.exit(1)
# signal.signal(signal.SIGINT, _sig_handler)
