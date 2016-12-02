import time


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            current_time = time.strftime("%Y-%m-%d %H:%M:%S ->", time.localtime())
            print current_time, text, ': Call %s() return %s' % (func.__name__, result)
            return result

        return wrapper

    return decorator
