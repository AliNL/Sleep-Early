# coding=utf-8
import os

from task import *


class Group(Task):
    def __init__(self, device):
        super(Group, self).__init__(device)
        self.name = 'Group fighting'

    @log("开始组队战斗")
    def start_group_fight(self):
        if self.d.exists('buying_energy.1334x750.png'):
            os.system('say -v Ting-Ting "体力不足"')
            self.analysis()
            raise Exception("体力不足")
        for t in range(3):
            if self.d.click_image('start_fighting.1334x750.png', timeout=1.0):
                time.sleep(2.5 + DELAY)
                if not self.d.exists('in_group.1334x750.png'):
                    return True
        return False

    @log("完成组队战斗")
    def group_fight(self):
        fighting(self)
        self.times += 1

    @log("点击确定")
    def ok(self):
        click_ok(self.d)

    @log("接受组队邀请")
    def get_invitation(self):
        click_get(self.d)

    @log("等待战斗开始")
    def wait_in_group(self):
        while in_group(self.d):
            pass
        if self.d.exists('buying_energy.1334x750.png'):
            os.system('say -v Ting-Ting "体力不足"')
            self.analysis()
            raise Exception("体力不足")
        return True

    def analysis(self):
        super(Group, self).analysis()
        print '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
