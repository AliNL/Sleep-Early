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

    @log("发现boss")
    def find_boss(self):
        for i in range(5):
            if self.d.exists('boss_icon.1334x750.png', threshold=0.9):
                return True
        return False

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

    @log("点击确定")
    def ok(self):
        click_ok(self.d)

    @log("接受组队邀请")
    def get_invitation(self):
        return click_get(self.d)

    def analysis(self):
        super(ExploreG, self).analysis()
