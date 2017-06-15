# coding=utf-8
from pages import get_image
from pages.base import BasePage


class Ground(BasePage):
    def __init__(self, driver=None, chapter=None, level=None, position=None, delay=0):
        super().__init__(driver, chapter, level, position, delay)
        self.d.keep_screen()
        if not self.d.exists("images/break_icon.1334x750.png"):
            raise AssertionError("不在探索地图")
        x, y = self.d.match(get_image('chapter_list.1334x750.png'), offset=(0, 1)).pos
        self.position['chapter_top'] = (x, y)
        self.position['chapter_bottom'] = (x, y + 4 * (self.position.l - x))
        self.position['back'] = self.d.match(get_image('back.1334x750.png')).pos
        self.position['break'] = self.d.match(get_image('break_icon.1334x750.png')).pos
        self.d.free_screen()

    def goto_yard(self):
        self.d.click(*self.position['back'])
        from pages.yard import Yard
        return Yard(*self.get_info())

    def goto_breaking(self):
        self.d.click_image("images/break_icon.1334x750.png", timeout=1)
        from pages.breaking import Breaking
        return Breaking(*self.get_info())

    def goto_chapter(self):
        import time
        image_name = get_image('C' + str(self.chapter) + '.1334x750.png')
        x1, y1 = self.position['chapter_top']
        x2, y2 = self.position['chapter_bottom']
        for t in range(-5, 5):
            if self.d.click_image(image_name, safe=True, threshold=0.9, timeout=1.0):
                self.wait_with_delay(2)
                from pages.chapter import Chapter
                return Chapter(*self.get_info())
            else:
                if t > 0:
                    self.d.swipe(x2, y2, x1, y1)
                else:
                    self.d.swipe(x1, y1, x2, y2)
            time.sleep(1)
        raise AssertionError("找不到章节")

    def get_big_box(self):
        for i in range(2):
            if self.d.click_image(get_image('big_treasure_box.1334x750.png'), safe=True, timeout=1.0):
                self.wait_with_delay(0.5)
                self.click_by_times(3)
                return
            else:
                self.wait_with_delay(0)
