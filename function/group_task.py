# coding=utf-8
from task import *


class Group(Task):
    def __init__(self):
        super(Group, self).__init__()

    @log("开始组队战斗")
    def start_group_fight(self):
        if not in_group(self.d):
            self.stop_reason = 'energy not enough'
            return False
        for t in range(3):
            if self.d.click_image('start_fighting.1334x750.png', timeout=1.0) is not None:
                time.sleep(3)
                if not self.d.exists('in_group.1334x750.png'):
                    return True
        return False

    @log("完成组队战斗")
    def group_fight(self):
        fighting(self)

    @log("点击确定")
    def click_ok(self):
        click_button(self.d, 'ok.1334x750.png', timeout=1.0)
        time.sleep(3)

    @log("等待战斗开始")
    def wait_in_group(self):
        while in_group(self.d):
            pass
        if in_yard(self.d):
            self.stop_reason = 'energy not enough'
            return False
        return True
