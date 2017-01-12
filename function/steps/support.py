# coding=utf-8
import time

import functools

import sys

device_delay = 0


def get_delay():
    return device_delay


def set_delay(value):
    global device_delay
    device_delay = value


def now(seconds=None):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds))


def log1(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print '%s -> %s: Call %s()' % (now(), text, func.__name__)
            return func(*args, **kw)

        return wrapper

    return decorator


def log2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print '%s -> 开始%s: Call %s()' % (now(), text, func.__name__)
            result = func(*args, **kw)
            print '%s -> 完成%s: Call %s() return %s' % (now(), text, func.__name__, result)
            print '-------------------------------------------------------------------------------------------------'
            return result

        return wrapper

    return decorator


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            print '%s -> %s: Call %s() return %s' % (now(), text, func.__name__, result)
            return result

        return wrapper

    return decorator


def log_refresh(text):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            sys.stdout.write('\r')
            sys.stdout.write('%s -> %s: Call %s() return %s' % (now(), text, func.__name__, result))
            sys.stdout.flush()
            if not result:
                sys.stdout.write('\n')
            return result

        return wrapper

    return decorator


def sure(func):
    @functools.wraps(func)
    def make_sure(*args, **kw):
        for i in range(0, 5):
            result = func(*args, **kw)
            time.sleep(0.5 + get_delay())
            if func(*args, **kw) == result:
                return result

    return make_sure


def click_button(d, *args, **kw):
    while not d.click_nowait(*args, **kw):
        pass
    while d.click_nowait(*args, **kw):
        pass


def click_once(d, *args, **kw):
    while not d.click_nowait(*args, **kw):
        pass
    d.click_nowait(*args, **kw)
