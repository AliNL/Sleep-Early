# coding=utf-8
from .task import *


class Challenge(Task):
    def __init__(self, device):
        super(Challenge, self).__init__(device)
        self.name = 'Challenge'

    @log("开始挑战")
    def start_challenge(self):
        if self.d.click_image(img('challenge'), timeout=3):
            time.sleep(2.5 + get_delay())
            if not self.d.exists(img('challenge')):
                return True
        return False

    @log("完成挑战")
    def challenge_fight(self):
        fighting(self, auto_ready=True)
        self.times += 1

    def analysis(self):
        super(Challenge, self).analysis()
        # print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
