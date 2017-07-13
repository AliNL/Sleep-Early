#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# License under MIT

from __future__ import absolute_import

import collections
import copy
import time
import warnings

import aircv as ac
import cv2
import os
import six

from atx import base
from atx import consts
from atx import errors
from atx import imutils
from atx import logutils
from atx.base import nameddict
from atx.drivers import Pattern, Bounds, FindPoint

warnings.simplefilter('default')

__dir__ = os.path.dirname(os.path.abspath(__file__))
log = logutils.getLogger(__name__)

Traceback = collections.namedtuple('Traceback', ['stack', 'exception'])
HookEvent = nameddict('HookEvent', ['flag', 'args', 'kwargs', 'retval', 'traceback', 'depth', 'is_before'])


# def hook_wrap(event_type):
#     def wrap(fn):
#         @functools.wraps(fn)
#         def _inner(*args, **kwargs):
#             func_args = inspect.getcallargs(fn, *args, **kwargs)
#             self = func_args.get('self')
#             self._depth += 1
#
#             def trigger(event):
#                 for (f, event_flag) in self._listeners:
#                     if event_flag & event_type:
#                         event.args = args[1:]
#                         event.kwargs = kwargs
#                         event.flag = event_type
#                         event.depth = self._depth
#                         f(event)
#
#             _traceback = None
#             _retval = None
#             try:
#                 trigger(HookEvent(is_before=True))
#                 _retval = fn(*args, **kwargs)
#                 return _retval
#             except Exception as e:
#                 _traceback = Traceback(traceback.format_exc(), e)
#                 raise
#             finally:
#                 trigger(HookEvent(is_before=False, retval=_retval, traceback=_traceback))
#                 self._depth -= 1
#
#         return _inner
#
#     return wrap


class DeviceMixin(object):
    def __init__(self):
        self.image_match_method = consts.IMAGE_MATCH_METHOD_TMPL
        self.image_match_threshold = 0.8
        self._resolution = None
        self._bounds = None
        self._listeners = []
        self.__last_screen = None
        self.__keep_screen = False
        self.__screensize = None

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        if value is None:
            self._resolution = None
        else:
            if not isinstance(value, tuple) or len(value) != 2:
                raise TypeError("Value should be tuple, contains two values")
            self._resolution = tuple(sorted(value))

    @property
    def last_screenshot(self):
        return self.__last_screen if self.__last_screen else self.screenshot()

    def _open_image_file(self, path):
        realpath = base.lookup_image(path, self.__screensize[0], self.__screensize[1])
        if realpath is None:
            raise IOError('file not found: {}'.format(path))
        return imutils.open(realpath)

    def pattern_open(self, image):
        if self.__screensize is None:
            self.__screensize = self.display

        if isinstance(image, Pattern):
            if image.image_ is None:
                image.image_ = self._open_image_file(image.name_)
            return image

        if isinstance(image, six.string_types):
            path = image
            return Pattern(path, image=self._open_image_file(path))

        if 'numpy' in str(type(image)):
            return Pattern('unknown', image=image)

        raise TypeError("Not supported image type: {}".format(type(image)))

    def delay(self, secs):
        secs = int(secs)
        time.sleep(secs)
        return self

    def exists(self, pattern, **match_kwargs):
        ret = self.match(pattern, **match_kwargs)
        if ret is None:
            return None
        if not ret.matched:
            return None
        return ret

    def wait(self, pattern, timeout=10.0, safe=False, **match_kwargs):
        t = time.time() + timeout
        while time.time() < t:
            ret = self.exists(pattern, **match_kwargs)
            if ret:
                return ret
            time.sleep(0.2)
        if not safe:
            raise errors.ImageNotFoundError('Not found image %s' % (pattern,))

    def wait_gone(self, pattern, timeout=10.0, safe=False, **match_kwargs):
        t = time.time() + timeout
        while time.time() < t:
            ret = self.exists(pattern, **match_kwargs)
            if not ret:
                return True
            time.sleep(0.2)
        if not safe:
            raise errors.ImageNotFoundError('Image not gone %s' % (pattern,))

    # def touch(self, x, y):
    #     self.click(x, y)

    def _cal_scale(self, pattern=None):
        scale = 1.0
        resolution = (pattern and pattern.resolution) or self.resolution
        if resolution is not None:
            ow, oh = sorted(resolution)
            dw, dh = sorted(self.display)
            fw, fh = 1.0 * dw / ow, 1.0 * dh / oh
            # For horizontal screen, scale by Y (width)
            # For vertical screen, scale by X (height)
            scale = fw if self.rotation in (1, 3) else fh
        return scale

    @property
    def bounds(self):
        if self._bounds is None:
            return None
        return self._bounds * self._cal_scale()

    def match_all(self, pattern, threshold=None):
        pattern = self.pattern_open(pattern)
        search_img = pattern.image

        pattern_scale = self._cal_scale(pattern)
        if pattern_scale != 1.0:
            search_img = cv2.resize(search_img, (0, 0),
                                    fx=pattern_scale, fy=pattern_scale,
                                    interpolation=cv2.INTER_CUBIC)

        threshold = threshold or pattern.threshold or self.image_match_threshold

        screen = self.region_screenshot()
        screen = imutils.from_pillow(screen)
        points = ac.find_all_template(screen, search_img, threshold=threshold, maxcnt=10)
        return points

    def match(self, pattern, screen=None, rect=None, offset=None, threshold=None, method=None):
        pattern = self.pattern_open(pattern)
        search_img = pattern.image

        pattern_scale = self._cal_scale(pattern)
        if pattern_scale != 1.0:
            search_img = cv2.resize(search_img, (0, 0),
                                    fx=pattern_scale, fy=pattern_scale,
                                    interpolation=cv2.INTER_CUBIC)

        screen = screen or self.region_screenshot()
        threshold = threshold or pattern.threshold or self.image_match_threshold

        # handle offset if percent, ex (0.2, 0.8)
        dx, dy = offset or pattern.offset or (0, 0)
        dx = pattern.image.shape[1] * dx  # opencv object width
        dy = pattern.image.shape[0] * dy  # opencv object height
        dx, dy = int(dx * pattern_scale), int(dy * pattern_scale)

        # image match
        screen = imutils.from_pillow(screen)  # convert to opencv image
        if rect and isinstance(rect, tuple) and len(rect) == 4:
            (x0, y0, x1, y1) = [v * pattern_scale for v in rect]
            (dx, dy) = dx + x0, dy + y0
            screen = imutils.crop(screen, x0, y0, x1, y1)
            # cv2.imwrite('cc.png', screen)

        match_method = method or self.image_match_method

        ret = None
        confidence = None
        matched = False
        if match_method == consts.IMAGE_MATCH_METHOD_TMPL:  # IMG_METHOD_TMPL
            ret = ac.find_template(screen, search_img)
            if ret is None:
                return None
            confidence = ret['confidence']
            if confidence > threshold:
                matched = True
            (x, y) = ret['result']
            position = (x + dx, y + dy)  # fix by offset
        else:
            ret_all = ac.find_all_template(screen, search_img, maxcnt=10)
            if not ret_all:
                return None
            for ret in ret_all:
                confidence = ret['confidence']
                if confidence > threshold:
                    (x, y) = ret['rectangle'][0]
                    color_screen = screen[y, x, 2]
                    color_img = search_img[0, 0, 2]
                    if -10 < int(color_img) - int(color_screen) < 10:
                        matched = True
                        break
            (x, y) = ret['result']
            position = (x + dx, y + dy)  # fix by offset

        if self.bounds:
            x, y = position
            position = (x + self.bounds.left, y + self.bounds.top)

        return FindPoint(position, confidence, match_method, matched=matched)

    def region(self, bounds):
        if not isinstance(bounds, Bounds):
            raise TypeError("region param bounds must be isinstance of Bounds")
        _d = copy.copy(self)
        _d._bounds = bounds
        return _d

    def keep_screen(self):
        self.__last_screen = self.screenshot()
        self.__keep_screen = True
        inner_self = self

        class _C(object):
            def __enter__(self):
                pass

            def __exit__(self, _type, value, _traceback):
                inner_self.free_screen()

        return _C()

    def free_screen(self):
        self.__keep_screen = False
        return self

    def region_screenshot(self, filename=None):
        screen = self.__last_screen if self.__keep_screen else self.screenshot()
        if self.bounds:
            screen = screen.crop(self.bounds)
        if filename:
            screen.save(filename)
        return screen

    # @hook_wrap(consts.EVENT_SCREENSHOT)
    def screenshot(self, filename=None):
        if self.__keep_screen:
            return self.__last_screen
        try:
            screen = self._take_screenshot()
        except IOError:
            log.warn("warning, screenshot failed [2/1], retry again")
            screen = self._take_screenshot()
        self.__last_screen = screen
        if filename:
            save_dir = os.path.dirname(filename) or '.'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            screen.save(filename)
        return screen

    # def touch_image(self, *args, **kwargs):
    #     self.click_image(*args, **kwargs)

    def add_listener(self, fn, event_flags):
        self._listeners.append((fn, event_flags))

    def _trigger_event(self, event_flag, event):
        for (fn, flag) in self._listeners:
            if flag & event_flag:
                fn(event)

    # @hook_wrap(consts.EVENT_CLICK_IMAGE)
    def click_nowait(self, pattern, action='click', **match_kwargs):
        point = self.match(pattern, **match_kwargs)
        if not point or not point.matched:
            return None

        func = getattr(self, action)
        func(*point.pos)
        return point

    def click_exists(self, *args, **kwargs):
        if len(args) > 0:
            return self.click_nowait(*args, **kwargs)
        else:
            elem = self(**kwargs)
            if elem.exists:
                return elem.click()

    # @hook_wrap(consts.EVENT_CLICK_IMAGE)
    def click_image(self, pattern, timeout=20.0, action='click', safe=False, desc=None, delay=None, **match_kwargs):
        pattern = self.pattern_open(pattern)
        log.info('click image:%s %s', desc or '', pattern)
        start_time = time.time()
        found = False
        point = None
        while time.time() - start_time < timeout:
            point = self.match(pattern, **match_kwargs)
            if point is None:
                continue

            log.debug('confidence: %s', point.confidence)
            if not point.matched:
                log.info('Ignore confidence: %s', point.confidence)
                continue

            # wait for program ready
            if delay and delay > 0:
                self.delay(delay)

            func = getattr(self, action)
            func(*point.pos)

            found = True
            break

        if not found:
            if safe:
                log.info("Image(%s) not found, safe=True, skip", pattern)
                return None
            raise errors.ImageNotFoundError('Not found image %s' % pattern, point)

        return point  # collections.namedtuple('X', ['pattern', 'point'])(pattern, point)

    @property
    def display(self):
        return []

    @property
    def rotation(self):
        return 0

    @rotation.setter
    def rotation(self, r):
        pass

    def _take_screenshot(self):
        return None

    def __call__(self, *args, **kwargs):
        return None


if __name__ == '__main__':
    b = Bounds(1, 2, 3, 4)
