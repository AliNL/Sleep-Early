# coding=utf-8
import time

import functools

import sys


def now(seconds=None):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds))


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
            time.sleep(1)
            if func(*args, **kw) == result:
                return result

    return make_sure


def click_button(d, *args, **kw):
    while not d.click_image(*args, **kw):
        pass
    while d.click_image(*args, **kw):
        pass
