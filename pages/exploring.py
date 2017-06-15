import time

from pages import get_image
from pages.base import BasePage


class Exploring(BasePage):
    def __init__(self, driver=None, chapter=None, level=None, position=None, delay=0):
        super().__init__(driver, chapter, level, position, delay)
        self.d.keep_screen()
        if not self.d.exists(get_image('exploring.1334x750.png')):
            raise AssertionError("不在副本地图")
        self.d.free_screen()

    def goto_fighting_boss(self):
        if self.d.click_image(get_image('boss_icon.1334x750.png'), safe=True, timeout=5.0):
            self.wait_with_delay(2.5)
            from pages.fighting import Fighting
            return Fighting(*self.get_info())
        return None

    def goto_fighting_monster(self):
        for i in range(-8, 8):
            self.d.free_screen()
            if self.d.click_image(get_image('monster_icon.1334x750.png'), safe=True, timeout=1.0):
                self.wait_with_delay(2.5)
                self.d.keep_screen()
                if self.d.exists(get_image('exploring.1334x750.png')):
                    if self.d.exists(get_image('buying_energy.1334x750.png')):
                        raise AssertionError("体力不足")
                    continue
                self.d.free_screen()
                from pages.fighting import Fighting
                return Fighting(*self.get_info())
            else:
                direction = 'left' if i > 0 else 'right'
                self.d.click(*self.position[direction])
                self.wait_with_delay(1.5)
        return None

    def get_small_boxes(self):
        while True:
            if self.d.exists("images/break_icon.1334x750.png"):
                from pages.ground import Ground
                return Ground(*self.get_info())
            boxes = self.d.match_all(get_image('small_treasure_box.1334x750.png'))
            if boxes:
                for box in boxes:
                    if box['confidence'] < 0.9:
                        break
                    self.d.click(*box['result'])
                    self.wait_with_delay(0.5)
                    self.click_by_times(1)
            time.sleep(1)
