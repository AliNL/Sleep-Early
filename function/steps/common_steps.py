# coding=utf-8
from support import *


@log_refresh("是否在组队中")
def in_group(d):
    if d.exists('in_group.1334x750.png'):
        return True
    return False


@log("是否在庭院内")
def in_yard(d):
    if d.exists('mail.1334x750.png'):
        return True
    return False


@log("是否在探索地图")
def in_explore_map(d):
    if d.exists('JueXing.1334x750.png'):
        return True
    return False


@log("是否在副本中")
def is_exploring(d):
    if d.exists('exploring.1334x750.png'):
        return True
    return False


@log("是否在阴阳寮结界突破")
def is_breaking(d):
    if d.exists('breaking.1334x750.png'):
        return True
    return False


@log1("继续")
def continue_(task, times=4):
    for t in range(times):
        task.d.click(*task.position.get('screen_bottom'))
        time.sleep(1 + get_delay())
    return True


@log_refresh("是否在战斗中")
def is_fighting(task):
    if task.d.exists('fighting.1334x750.png'):
        task.d.click(*task.position.get('mid'))
        return True
    if task.d.exists('ready.1334x750.png'):
        return True
    return False


def is_not_ready(d):
    if d.exists('not_ready.1334x750.png'):
        return True
    return False


@log("自动准备")
def get_ready(d):
    if d.exists('not_ready.1334x750.png'):
        d.click_image('ready_icon.1334x750.png', timeout=1.0)
        time.sleep(1)
        return True
    return False


def fighting(task, times=4, auto_ready=False):
    if auto_ready:
        task.d.click_image('ready_icon.1334x750.png', timeout=20.0)
    else:
        time.sleep(2)
    while not is_fighting(task):
        if get_ready(task.d):
            break
    while is_fighting(task):
        pass
    get_bonus_task(task.d)
    continue_(task, times)
    return True


def get_bonus_task(d):
    d.click_image('bonus_task.1334x750.png', timeout=1.0, offset=(1, 6.5))


@log("点击确定")
def click_ok(d):
    if d.click_image('confirm.1334x750.png', timeout=90.0):
        time.sleep(3)
        return True
    else:
        return False


@log("接受组队邀请")
def click_get(d):
    if d.click_image('cancel.1334x750.png', offset=(2, 0), timeout=90.0):
        time.sleep(3)
        return True
    else:
        return False
