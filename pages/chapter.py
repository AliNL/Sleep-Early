from pages import get_image
from pages.base import BasePage


class Chapter(BasePage):
    def __init__(self, driver=None, chapter=None, level=None, position=None):
        super().__init__(driver, chapter, level, position)
        self.d.keep_screen()
        if not self.d.exists("images/explore_icon.1334x750.png"):
            raise AssertionError("选取章节失败")
        self.position['challenge'] = self.d.match(get_image('explore_icon.1334x750.png')).pos
        self.position['chapter_close'] = self.d.match(get_image('close.1334x750.png')).pos
        self.d.free_screen()

    def goto_exploring(self):
        self.d.click(*self.position['challenge'])
        self.wait_with_delay(2)
        from pages.exploring import Exploring
        return Exploring(*self.get_info())

    def goto_ground(self):
        self.d.click(*self.position['chapter_close'])
        self.wait_with_delay(1)
        from pages.ground import Ground
        return Ground(*self.get_info())
