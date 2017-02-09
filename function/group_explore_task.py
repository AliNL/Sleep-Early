# coding=utf-8
import os
from explore_task import *
from steps import *


class ExploreG(Explore):
    def __init__(self, device):
        super(ExploreG, self).__init__(1, device)
        self.name = 'Group Explore'
        self.monster_killed = 0
        self.small_box = 0
        self.big_box = 0
        self.stop_reason = 'task completed'

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

    @log2("打boss")
    def __fight_boss(self):
        for t in range(3):
            if self.d.click_image('boss_icon.1334x750.png', threshold=0.9, timeout=1.0, delay=3.0):
                time.sleep(2.5 + get_delay())
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

    @log("点击确定")
    def ok(self):
        click_ok(self.d)

    @log("接受组队邀请")
    def get_invitation(self):
        return click_get(self.d)

    def analysis(self):
        super(ExploreG, self).analysis()
