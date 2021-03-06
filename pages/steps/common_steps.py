# coding=utf-8
from pages.steps.path_manager import img
from .support import *


@log_refresh("是否在组队中")
def in_group(d):
    time.sleep(0.5 + get_delay())
    return not not d.exists(img('in_group'))


@log("是否在庭院内")
def in_yard(d):
    time.sleep(0.5 + get_delay())
    return not not d.exists(img('mail'))


@log("是否在探索地图")
def in_explore_map(d):
    time.sleep(0.5 + get_delay())
    return not not d.exists(img('JueXing'))


@log("是否在副本中")
def is_exploring(d):
    time.sleep(0.5 + get_delay())
    return not not d.exists(img('exploring'))


@log("是否在阴阳寮结界突破")
def is_breaking(d):
    time.sleep(0.5 + get_delay())
    return not not d.exists(img('breaking'))


def is_not_ready(d):
    time.sleep(0.5 + get_delay())
    return not not d.exists(img('not_ready'))


@log1("继续")
def continue_(task, times=4):
    for t in range(times):
        x, y = task.position.get('screen_bottom')
        task.d.click(x + t, y + t)
        time.sleep(0.7 + get_delay())
    return True


@log_refresh("是否在战斗中")
@sure
def is_fighting(task):
    if task.d.exists(img('fighting')):
        # task.d.click(*task.position.get('mid'))
        return True
    if task.d.exists(img('ready')):
        return True
    return False


@log("自动准备")
@freeze
def get_ready(d):
    if d.exists(img('not_ready')):
        d.click_nowait(img('ready_icon'))
        time.sleep(1 + get_delay())
        return True
    return False


def fighting(task, times=4, auto_ready=False):
    if auto_ready:
        task.d.click_image(img('ready_icon'), timeout=20.0)
    else:
        time.sleep(1.5 + get_delay())
    while not is_fighting(task):
        if get_ready(task.d):
            break
    while is_fighting(task):
        pass
    get_bonus_task(task.d)
    continue_(task, times)
    return True


def get_bonus_task(d):
    d.click_image(img('bonus_task'), safe=True, timeout=1.0, offset=(1, 6.5))


@log("点击确定")
def click_ok(d):
    if d.click_image(img('confirm'), timeout=90.0):
        time.sleep(3 + get_delay())
        return True
    else:
        return False


@log("接受组队邀请")
def click_get(d):
    if d.click_image(img('cancel'), offset=(2, 0), timeout=60.0):
        time.sleep(3 + get_delay())
        return True
    else:
        return False
