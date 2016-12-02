# coding=utf-8
from steps import *


class Explore(object):
    def __init__(self, chapter, driver):
        super(Explore, self).__init__()
        self.d = driver
        self.chapter = chapter
        self.monster_killed = 0
        self.small_box = 0
        self.big_box = 0
        self.position = Position(driver)

    def __scroll_to_chapter(self):
        image_name = 'C' + str(self.chapter) + '.1334x750.png'
        for t in range(5, -5):
            if self.d.click_image(image_name, threshold=0.85, timeout=2.0) is not None:
                time.sleep(1)
                self.d.click_image('explore_icon.1334x750.png')
                time.sleep(3)
                return True
            else:
                x1, y1 = self.position['chapter_top']
                x2, y2 = self.position['chapter_bottom']
                if t > 0:
                    self.d.swipe(x1, y1, x2, y2)
                else:
                    self.d.swipe(x2, y2, x1, y1)
            time.sleep(1)
        return False

    @log("选择探索章节")
    def choose_chapter(self):
        if 0 < self.chapter < 19:
            return self.__scroll_to_chapter()
        else:
            raise IOError("Invalid chapter number!!!")

    @log("打小怪")
    def fight_monster(self):
        for i in range(8, -8):
            if self.d.click_image('monster_icon.1334x750.png', timeout=1.0) is not None:
                time.sleep(3)
                if self.d.exists('exploring.1334x750.png'):
                    return False
                return fighting(self.d)
            else:
                direction = 'right' if i > 0 else 'left'
                self.d.click(*self.position[direction])
                time.sleep(2)
        return False

    @log("打boss")
    def fight_boss(self):
        for t in range(3):
            if self.d.click_image('boss_icon.1334x750.png', timeout=1.0) is not None:
                time.sleep(3)
                if self.d.exists('exploring.1334x750.png'):
                    return False
                return fighting(self.d)
        return False

    @log("捡小宝箱")
    def get_small_box(self):
        if self.d.click_image('small_treasure_box.1334x750.png', timeout=1.0) is not None:
            time.sleep(1)
            continue_(self, 1)
            return True
        else:
            return False

    @log("捡大宝箱")
    def get_big_box(self):
        for i in range(2):
            if self.d.click_image('big_treasure_box.1334x750.png', timeout=1.0) is not None:
                time.sleep(1)
                continue_(self, 2)
                self.big_box += 1
                return True
            else:
                time.sleep(0.5)
        return False

    @log("查找石距")
    @sure
    def find_shi_ju(self):
        if self.d.exists('shi_ju.1334x750.png'):
            return True
        return False
