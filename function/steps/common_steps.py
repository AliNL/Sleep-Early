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
    if d.exists('fighting.1334x750.png'):
        return True
    if d.exists('ready.1334x750.png'):
        return True
    return False


@log("等待准备")
@sure
def is_not_ready(d):
    if d.exists('not_ready.1334x750.png'):
        return True
    return False


def get_ready(d):
    if is_not_ready(d):
        d.click_image('ready_icon.1334x750.png', offset=(0, -1.5))


def fighting(task, times=4):
    while not is_fighting(task.d):
        get_ready(task.d)
    while is_fighting(task.d):
        pass
    continue_(task, times)
    return True
