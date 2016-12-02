# coding=utf-8
import functools
import time
from get_log import log


def sure(func):
    @functools.wraps(func)
    def make_sure(*args, **kw):
        for i in range(0, 5):
            result = func(*args, **kw)
            time.sleep(1)
            if func(*args, **kw) == result:
                return result

    return make_sure


@log("是否登陆成功")
def logged_in(d):
    while not d.exists("mail.1334x750.png"):
        time.sleep(2)
    return True


@log("是否在探索地图")
@sure
def in_explore_map(d):
    if d.exists('JueXing.1334x750.png'):
        return True
    return False


@log("是否在战斗中")
@sure
def is_fighting(d):
    if d.exists('fighting.1334x750.png'):
        return True
    if d.exists('ready.1334x750.png'):
        return True
    return False


@log("是否战斗胜利")
def success(d):
    if d.exists('success.1334x750.png'):
        return True
    return False


@log("是否在选择式神")
@sure
def is_switching(d):
    if d.exists('switching.1334x750.png'):
        return True
    return False


@log("等待准备")
def is_not_ready(d):
    if d.exists('not_ready.1334x750.png'):
        return True
    return False


@log("是否发现石距")
@sure
def is_shiju_found(d):
    if d.exists('shi_ju.1334x750.png'):
        return True
    return False

