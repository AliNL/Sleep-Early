# coding=utf-8
from .task import *


class Group(Task):
    def __init__(self, device):
        super(Group, self).__init__(device)
        self.name = 'Group fighting'

    @log("开始组队战斗")
    def start_group_fight(self):
        if self.d.exists(img('buying_energy')):
            return False
        if self.d.click_image(img('start_fighting')):
            time.sleep(2.5 + get_delay())
            if not self.d.exists(img('in_group')):
                return True
        return False

    @log("完成组队战斗")
    def group_fight(self):
        fighting(self, auto_ready=True)
        self.times += 1

    @log("等待战斗开始")
    def wait_in_group(self):
        while in_group(self.d):
            pass
        if self.d.exists(img('buying_energy')):
            self.analysis()
            raise Exception("体力不足")
        return True

    def analysis(self):
        super(Group, self).analysis()
        # print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
