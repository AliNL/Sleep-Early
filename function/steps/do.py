# coding=utf-8
import time

from find import *
from support import log


@log("查找章节")
def scroll_to_chapter(option, times, num, d):
    image_name = 'C' + str(num) + '.1334x750.png'
    for t in range(0, times):
        if d.click_image(image_name, threshold=0.85, timeout=2.0) is not None:
            d.click_image('explore_icon.1334x750.png')
            time.sleep(3)
            return True
        else:
            if option == 0:
                d.swipe(740, 205, 740, 450)
                # d.swipe(1230, 200, 1230, 500, duration=0.1)
            else:
                d.swipe(740, 450, 740, 205)
                # d.swipe(1230, 500, 1230, 200, duration=0.1)
            time.sleep(1)
    return False


@log("选择章节")
def choose_chapter(num, d):
    if 0 < num < 19:
        if scroll_to_chapter(0, 4, num, d):
            return True
        else:
            return scroll_to_chapter(1, 4, num, d)
    else:
        return False


@log("继续")
def continue_(d, times=3):
    for t in range(times):
        d.click(100, 100)
        # d.click(d.display[0] / 2, d.display[1] * 0.9)
        time.sleep(1.5)
    return True


@log("战斗准备完毕")
def get_ready(d):
    while is_switching(d):
        pass
    if is_not_ready(d):
        d.click_image('ready_icon.1334x750.png', offset=(0, -1.5))
    return True


@log("战斗完毕")
def fighting(d, times=4):
    while not is_fighting(d):
        get_ready(d)
    while is_fighting(d):
        pass
    continue_(d, times)
    return True


@log("打了小怪")
def fight(d):
    for i in range(0, 8):
        if d.click_image('monster_icon.1334x750.png', timeout=1.0) is not None:
            time.sleep(3)
            if d.exists('exploring.1334x750.png'):
                return False
            return fighting(d)
        else:
            d.click_image('exploring.1334x750.png', offset=(0.8, -1))
            time.sleep(3)
        continue
    return False


@log("打了Boss")
def fight_boss(d):
    for t in range(3):
        if d.click_image('boss_icon.1334x750.png', timeout=1.0) is not None:
            time.sleep(0.5)
            if d.exists('exploring.1334x750.png'):
                return False
            return fighting(d)
    return False


@log("捡了小宝箱")
def open_small_treasure_box(d):
    if d.click_image('small_treasure_box.1334x750.png', timeout=3.0) is not None:
        time.sleep(1)
        continue_(d, 1)
        return True
    else:
        time.sleep(1)
        return False


@log("捡了大宝箱")
def open_big_treasure_box(d):
    for i in range(2):
        if d.click_image('big_treasure_box.1334x750.png', timeout=1.0) is not None:
            time.sleep(1)
            continue_(d, 2)
            return True
        else:
            time.sleep(0.5)
    return False


@log("组队战斗开始")
def start_fighting(d):
    while d.click_image('start_fighting.1334x750.png', timeout=1.0, delay=3.0) is None:
        time.sleep(1)
    return True


@log("继续邀请组员")
def invite(d):
    while d.click_image('ok.1334x750.png', timeout=1.0) is None:
        time.sleep(1)
    return True


@log("接受战斗邀请")
def get_invited(d):
    while d.click_image('ok.1334x750.png', timeout=1.0) is None:
        time.sleep(1)
    return True


@log("切换目标阴阳寮")
def choose_group(g, d):
    d.click(300, 180 * (g + 1))
    time.sleep(1)
    return g + 1


def find_under_level(l, d):
    if l > 7:
        l /= 10
    for i in range(l):
        img = 'level_' + str(i) + '.1334x750.png'
        if d.click_image(img, threshold=0.9, timeout=1.0) is not None:
            time.sleep(1)
            d.click_image('attack.1334x750.png', timeout=1.0)
            return True
    return False


@log("寻找低等级目标")
def find_under_level_scroll(l, d):
    while True:
        if find_under_level(l, d):
            return True
        else:
            if d.exists('broken.1334x750.png'):
                break
            d.swipe(600, 540, 600, 180, duration=0.1)
            time.sleep(1)
    return False
