# coding=utf-8
from support import *


@log_refresh("是否在组队中")
@sure
def in_group(d):
    if d.exists('in_group.1334x750.png'):
        return True
    return False


@log("是否在庭院内")
@sure
def in_yard(d):
    if d.exists('mail.1334x750.png'):
        return True
    return False


@log("是否在探索地图")
@sure
def in_explore_map(d):
    if d.exists('JueXing.1334x750.png'):
        return True
    return False


@log("是否在副本中")
@sure
def is_exploring(d):
    if d.exists('exploring.1334x750.png'):
        return True
    return False


@log("是否在阴阳寮结界突破")
@sure
def is_breaking(d):
    if d.exists('breaking.1334x750.png'):
        return True
    return False


@log("继续")
def continue_(task, times=4):
    for t in range(times):
        task.d.click(*task.position.get('screen_bottom'))
        time.sleep(1.5)
    return True


@log_refresh("是否在战斗中")
def is_fighting(d):
    if is_not_ready(d):
        return False
    if d.exists('fighting.1334x750.png'):
        return True
    if d.exists('ready.1334x750.png'):
        return True
    return False


# @log_refresh("是否在选择式神")
# @sure
# def is_switching(d):
#     if d.exists('switching.1334x750.png'):
#         return True
#     return False


def is_not_ready(d):
    if d.exists('not_ready.1334x750.png'):
        return True
    return False


@log("自动准备")
def get_ready(d):
    if d.click_image('ready_icon.1334x750.png', timeout=1.0, offset=(0.3, -1.5)) is not None:
        return True
    return False


def fighting(task, times=4):
    while not is_fighting(task.d):
        if get_ready(task.d):
            break
    while is_fighting(task.d):
        pass
    get_bonus_task(task.d)
    while is_fighting(task.d):
        pass
    continue_(task, times)
    return True


def get_bonus_task(d):
    d.click_image('bonus_task.1334x750.png', timeout=1.0, offset=(1, 6.5))
