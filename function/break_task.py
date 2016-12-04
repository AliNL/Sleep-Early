# coding=utf-8
from task import *
from steps import *


class Break(Task):
    def __init__(self, level):
        if not 0 < level < 8:
            raise IOError("Invalid level!!!")
        super(Break, self).__init__()
        self.name = 'Public breaking'
        self.level = level
        self.target = 0
        self.broken = [0, 0, 0]

    @log("切换目标阴阳寮")
    def __choose_group(self):
        x, y = self.position.get('first_target')
        self.target = 1 if self.target == 3 else (self.target + 1)
        self.d.click(x, y * self.target)
        time.sleep(1)
        return self.target

    def __find_under_level(self):
        for i in range(self.level):
            img = 'level_' + str(i) + '.1334x750.png'
            if self.d.click_image(img, threshold=0.9, timeout=1.0) is not None:
                time.sleep(1)
                self.d.click_image('attack.1334x750.png', timeout=1.0)
                return True
        return False

    @log2("寻找低等级目标")
    def __find_under_level_scroll(self):
        while True:
            if self.__find_under_level():
                return True
            else:
                if self.d.exists('broken.1334x750.png'):
                    break
                x1, y1 = self.position.get('break_top')
                x2, y2 = self.position.get('break_bottom')
                self.d.swipe(x2, y2, x1, y1)
                time.sleep(1)
        return False

    def breaking(self):
        while 0 in self.broken:
            self.__choose_group()
            if self.__find_under_level_scroll():
                time.sleep(2)
                if not self.d.exists('level_6.1334x750.png'):
                    fighting(self, 3)
                    self.times += 1
                else:
                    self.d.click_image('black_icon.1334x750.png')
                    self.d.delay(20)
            else:
                self.broken[self.target - 1] = 1
                print '第%d个阴阳寮刷完了' % self.target
            self.analysis()
            self.d.delay(180)

    def analysis(self):
        super(Break, self).analysis()
        print '┃%31s%-19s┃' % ('level: under ', self.level * 10)
        print '┃%25s%-25s┃' % ('broken: ', self.broken)
        print '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
