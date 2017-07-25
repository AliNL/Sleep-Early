# coding=utf-8
import functools
import time

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
            # print('%s -> %s: Call %s()' % (now(), text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


def log2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            # print('%s -> 开始%s: Call %s()' % (now(), text, func.__name__))
            result = func(*args, **kw)
            # print('%s -> 完成%s: Call %s() return %s' % (now(), text, func.__name__, result))
            # print('-------------------------------------------------------------------------------------------------')
            return result

        return wrapper

    return decorator


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            # print('%s -> %s: Call %s() return %s' % (now(), text, func.__name__, result))
            return result

        return wrapper

    return decorator


def log_underline(text):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            # print('%s -> %s: Call %s() return %s' % (now(), text, func.__name__, result))
            # print('-------------------------------------------------------------------------------------------------')
            return result

        return wrapper

    return decorator


def log_refresh(text):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            # sys.stdout.write('\r')
            # sys.stdout.write('%s -> %s: Call %s() return %s' % (now(), text, func.__name__, result))
            # sys.stdout.flush()
            if not result:
                pass
                # sys.stdout.write('\n')
            return result

        return wrapper

    return decorator


def sure(func):
    @functools.wraps(func)
    def make_sure(*args, **kw):
        for i in range(5):
            result = func(*args, **kw)
            if result:
                return True
            time.sleep(0.5 + get_delay())
            if not func(*args, **kw):
                return False

    return make_sure


def freeze(func):
    @functools.wraps(func)
    def keep(d, *args, **kw):
        d.keep_screen()
        result = func(d, *args, **kw)
        d.free_screen()
        return result

    return keep
