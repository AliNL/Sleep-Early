# coding=utf-8
from support import log
from common_steps import *


class Position(dict):
    def __init__(self, driver, **kwargs):
        super(Position, self).__init__(**kwargs)
        self.d = driver
        self.w, self.l = sorted(driver.display)
        self['screen_bottom'] = (self.l / 2, self.w * 0.85)

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
        if in_explore_map(self.d):
            x, y = self.d.match('chapter_list.1334x750.png', offset=(0, 1))[0]
            self['chapter_top'] = (x, y)
            self['chapter_bottom'] = (x, y + 4 * (self.l - x))
            return True
        elif is_exploring(self.d):
            x, y = self.d.match('exploring.1334x750.png', offset=(0.8, -1))[0]
            self['right'] = (x, y)
            self['left'] = (self.l - x, y)
            return True
        elif is_breaking(self.d):
            x, y = self.d.match('breaking.1334x750.png', offset=(0.8, 2.5))[0]
            self['first_target'] = (x, y * 0.25)
            self['break_top'] = (self.l - x, y * 0.25)
            self['break_bottom'] = (self.l - x, y * 0.75)
            return True
        return False
