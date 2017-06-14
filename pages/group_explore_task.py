# coding=utf-8
from .explore_task import *
from .steps import *


class ExploreG(Explore):
    def __init__(self, device):
        super(ExploreG, self).__init__(1, device)
        self.name = 'Group Explore'
        self.monster_killed = 0
        self.small_box = 0
        self.big_box = 0
        self.stop_reason = 'task completed'

    @log("发现boss")
    def find_boss(self):
        return self.d.wait('boss_icon.1334x750.png', threshold=0.9, timeout=4)

    def exploring_wait(self):
        while not self.find_boss():
            while is_exploring(self.d):
                pass
            fighting(self)
            self.monster_killed += 1
        while is_exploring(self.d):
            pass
        fighting(self)
        self.times += 1

    def analysis(self):
        super(ExploreG, self).analysis()
