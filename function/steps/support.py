# coding=utf-8
import time

import functools


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S ->", time.localtime())


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print '%s 正在%s: Call %s()' % (now(), text, func.__name__)
            result = func(*args, **kw)
            print '%s 完成%s: Call %s() return %s' % (now(), text, func.__name__, result)
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
