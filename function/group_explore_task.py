# coding=utf-8
import os
from task import *
from steps import *


class ExploreG(Task):
    def __init__(self, device):
        super(ExploreG, self).__init__(device)
        self.name = 'Group Explore'
        self.monster_killed = 0
        self.small_box = 0
        self.big_box = 0
        self.stop_reason = 'task completed'

    @log2("打小怪")
    def __fight_monster(self):
        for i in range(-8, 8):
            if self.d.click_image('monster_icon.1334x750.png', threshold=0.9, timeout=1.0):
                time.sleep(3)
                if is_exploring(self.d):
                    if self.d.exists('buying_energy.1334x750.png'):
                        os.system('say -v Ting-Ting "体力不足"')
                        self.analysis()
                        raise Exception("体力不足")
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
            if self.d.click_image('boss_icon.1334x750.png', threshold=0.9, timeout=1.0, delay=3.0):
                time.sleep(3)
                if is_exploring(self.d):
                    if self.d.exists('buying_energy.1334x750.png'):
                        os.system('say -v Ting-Ting "体力不足"')
                        self.analysis()
                        raise Exception("体力不足")
                    continue
                fighting(self)
                self.times += 1
                return True
        return False

    def exploring_fight(self):
        while not self.__fight_boss():
            self.__fight_monster()
        while self.__fight_boss():
            pass

    def exploring_wait(self):
        while not find_boss(self.d):
            while is_exploring(self.d):
                pass
            fighting(self)
            self.monster_killed += 1
        while is_exploring(self.d):
            pass
        fighting(self)
        self.times += 1

    @log2("捡小宝箱")
    def get_small_box(self):
        while not in_explore_map(self.d):
            if self.d.click_image('small_treasure_box.1334x750.png', timeout=1.0):
                time.sleep(1)
                continue_(self, 1)
                self.small_box += 1

    @log("是否体力不足")
    def is_pl_not_enough(self):
        if self.d.exists('no_enough_pl.1334x750.png', threshold=0.95):
            self.stop_reason = 'energy not enough'
            self.analysis()
            return True
        return False

    @log("点击确定")
    def ok(self):
        click_ok(self.d)

    @log("接受组队邀请")
    def get_invitation(self):
        click_get(self.d)

    def analysis(self):
        super(ExploreG, self).analysis()
        print '┃%25s%-25s┃' % ('monster killed: ', self.monster_killed)
        print '┃%25s%-25s┃' % ('small box: ', self.small_box)
        print '┃%25s%-25s┃' % ('big box: ', self.big_box)
        print '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
