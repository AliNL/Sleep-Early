# coding=utf-8
from task import *
from steps import *


class Explore(Task):
    def __init__(self, chapter):
        if not 0 < chapter < 19:
            raise IOError("Invalid chapter number!!!")
        super(Explore, self).__init__()
        self.name = 'Explore'
        self.chapter = chapter
        self.monster_killed = 0
        self.small_box = 0
        self.big_box = 0
        self.stop_reason = 'task completed'

    def end_fighting(self):
        return is_exploring(self.d)

    @log2("选择探索章节")
    def choose_chapter(self):
        image_name = 'C' + str(self.chapter) + '.1334x750.png'
        navigate_to_explore_map(self.d)
        for t in range(-5, 5):
            if self.d.click_image(image_name, threshold=0.9, timeout=1.0) is not None:
                time.sleep(1)
                if self.d.click_image('explore_icon.1334x750.png') is not None:
                    time.sleep(3)
                    return True
            else:
                x1, y1 = self.position.get('chapter_top')
                x2, y2 = self.position.get('chapter_bottom')
                if t > 0:
                    self.d.swipe(x2, y2, x1, y1)
                else:
                    self.d.swipe(x1, y1, x2, y2)
            time.sleep(1)

    @log2("打小怪")
    def __fight_monster(self):
        for i in range(-8, 8):
            if self.d.click_image('monster_icon.1334x750.png', threshold=0.9, timeout=1.0) is not None:
                time.sleep(3)
                if is_exploring(self.d):
                    continue
                if fighting(self):
                    self.monster_killed += 1
                    return True
            else:
                direction = 'left' if i > 0 else 'right'
                self.d.click(*self.position.get(direction))
                time.sleep(2)
        return False

    @log2("打boss")
    def __fight_boss(self):
        for t in range(3):
            if self.d.click_image('boss_icon.1334x750.png', threshold=0.9, timeout=1.0) is not None:
                time.sleep(3)
                if is_exploring(self.d):
                    return False
                if fighting(self):
                    self.times += 1
                    return True
        return False

    def exploring_fight(self):
        for t in range(3):
            self.__fight_monster()
        while not self.__fight_boss():
            self.__fight_monster()
        while self.__fight_boss():
            pass

    @log2("捡小宝箱")
    def get_small_box(self):
        while not in_explore_map(self.d):
            if self.d.click_image('small_treasure_box.1334x750.png', timeout=1.0) is not None:
                time.sleep(1)
                continue_(self, 1)
                self.small_box += 1

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
    def found_shi_ju(self):
        if self.d.exists('shi_ju.1334x750.png'):
            self.stop_reason = 'shi ju found'
            self.analysis()
            return True
        return False

    @log("是否体力不足")
    def is_pl_not_enough(self):
        if self.d.exists('no_enough_pl.1334x750.png', threshold=0.95):
            self.stop_reason = 'energy not enough'
            self.analysis()
            return True
        return False

    def analysis(self):
        super(Explore, self).analysis()
        print '┃%25s%-25s┃' % ('monster killed: ', self.monster_killed)
        print '┃%25s%-25s┃' % ('small box: ', self.small_box)
        print '┃%25s%-25s┃' % ('big box: ', self.big_box)
        print '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
