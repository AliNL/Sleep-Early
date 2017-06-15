# coding=utf-8
from .common_steps import *


class Position(dict):
    def __init__(self, driver, **kwargs):
        super(Position, self).__init__(**kwargs)
        self.d = driver
        self.w, self.l = sorted(driver.display)
        self['screen_bottom'] = (self.l * 0.75, self.w * 0.8)
        self['right'] = (self.l * 0.9, self.w * 0.8)
        self['left'] = (self.l * 0.1, self.w * 0.8)
        self['mid'] = (self.l * 0.5, self.w * 0.3)

    def get(self, k, d=None):
        if k not in self:
            if self.set_up():
                return self[k]
            else:
                raise IOError("Unable to get position!!!")
        else:
            return self[k]

    @log("获取屏幕坐标")
    def set_up(self):
        self.d.keep_screen()
        if in_explore_map(self.d):
            x, y = self.d.match(img('chapter_list'), offset=(0, 1))[0]
            self['chapter_top'] = (x, y)
            self['chapter_bottom'] = (x, y + 4 * (self.l - x))
            self.d.free_screen()
            return True
        elif is_breaking(self.d):
            self['first_target'] = (self.l * 0.25, self.w * 0.25)
            self['break_top'] = (self.l * 0.75, self.w * 0.25)
            self['break_bottom'] = (self.l * 0.75, self.w * 0.75)
            self.d.free_screen()
            return True
        self.d.free_screen()
        return False
