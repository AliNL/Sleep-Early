import time

from pages import get_image
from pages.base import BasePage


class Fighting(BasePage):
    def __init__(self, driver=None, chapter=None, level=None, position=None, delay=0):
        super().__init__(driver, chapter, level, position, delay)
        self.d.keep_screen()
        if self.d.exists(get_image('exploring.1334x750.png')):
            raise AssertionError("进入战斗失败")
        self.d.free_screen()

    def get_ready(self):
        time.sleep(2)
        self.d.keep_screen()
        if self.d.exists(get_image('not_ready.1334x750.png')):
            self.d.click_nowait(get_image('ready_icon.1334x750.png'))
        self.d.free_screen()
        time.sleep(1)

    def auto_ready(self):
        self.d.click_image(get_image('ready_icon.1334x750.png'), timeout=20.0)

    def is_fighting(self):
        if self.d.exists(get_image('fighting.1334x750.png')):
            self.d.click(*self.position.get('mid'))
            return True
        if self.d.exists(get_image('ready.1334x750.png')):
            return True
        return False

    def wait_and_continue(self):
        while not self.is_fighting():
            self.get_ready()
        while self.is_fighting():
            pass
        self.d.click_image(get_image('bonus_task.1334x750.png'), safe=True, timeout=1.0, offset=(1, 6.5))
        self.click_by_times(4)
        from pages.exploring import Exploring
        return Exploring(*self.get_info())
