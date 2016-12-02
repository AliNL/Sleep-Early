# coding=utf-8
from find import *
from support import log


class PointsList(dict):
    def __init__(self, driver, iterable=None, **kwargs):
        super(PointsList, self).__init__(iterable, **kwargs)
        self.d = driver

    def get(self, k, de=None):
        if k not in self:
            self.set_up(self.d)

    @log("获取屏幕坐标")
    def set_up(self):
        w, l = sorted(self.d.display)
        if in_explore_map(self.d):
            x1, y1 = self.d.match('chapter_list.1334x750.png')[0]
            self['list_top'] = (x1, y1 + l - x1)
            self['list_bottom'] = (x1, y1 + 4.5 * (l - x1))
            self['screen_bottom'] = (l / 2, w * 0.9)
            return True
            # elif is_breaking(d):
            #     pass
