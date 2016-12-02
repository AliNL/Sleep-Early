# coding=utf-8
import os
import wda
import atx
from steps import *

driver = None


def launch():
    global driver
    try:
        driver = atx.connect()
    except Exception:
        fl = open('session_id_ios')
        sid = fl.read()
        fl.close()
        driver = atx.connect('http://localhost:8100')
        driver._session = wda.Session('http://localhost:8100', sid)
    driver.image_path = ['.', 'images']
    return driver


def easy_explore(chapter_number):
    global driver
    monster_killed = 0
    while not in_explore_map(driver):
        pass
    while not choose_chapter(chapter_number, driver):
        pass
    while True:
        if monster_killed >= 3 and fight_boss(driver):
            break
        else:
            if fight(driver):
                monster_killed += 1
    while not in_explore_map(driver):
        open_small_treasure_box(driver)
    open_big_treasure_box(driver)
    if is_shiju_found(driver):
        os.system('say "congratulations"')
        return False
    return True


def easy_group(is_lead):
    global driver
    if is_lead:
        while not start_fighting(driver):
            pass
        fighting(driver)
        invite(driver)
    else:
        fighting(driver)
        get_invited(driver)


def easy_public_breaking(level_10):
    global driver
    finish = [0, 0, 0]
    while 0 in finish:
        for g in range(3):
            choose_group(g, driver)
            if find_under_level_scroll(level_10, driver):
                time.sleep(2)
                if not driver.exists('level_6.1334x750.png'):
                    fighting(driver, 3)
                else:
                    driver.click_image('black_icon.1334x750.png')
                    driver.delay(20)
            else:
                finish[g] = 1
                print '第%d个阴阳寮刷完了' % (g + 1)
            driver.delay(180)
