# coding=utf-8
from task import *
from steps import *


class Break(Task):
    def __init__(self, time_, level=7, target=1, device='android'):
        if not 0 < level < 8:
            raise IOError("Invalid level!!!")
        super(Break, self).__init__(device)
        self.name = 'Public breaking'
        self.start = time.time()
        self.time_ = time_ * 3600
        self.level = level
        self.target = target - 1
        self.broken = [0, 0, 0]
        self.last = 0

    def wait(self):
        begin = self.last + 195
        while time.time() < begin:
            self.d.click_image('busy.1334x750.png', timeout=1.0)
            get_bonus_task(self.d)
            sys.stdout.write('\r')
            sys.stdout.write('%s -> wait until %s' % (now(), now(begin)))
            sys.stdout.flush()
        sys.stdout.write('\n')

    @log("突破券充足")
    def if_tickets_enough(self):
        if self.d.exists('no_tickets.1334x750.png', threshold=0.95):
            return False
        return True

    @log("完成个人结界突破")
    def finish_personal_breaking(self):
        if self.d.wait('get_bonus.1334x750.png', threshold=0.9,timeout=5.0):
            continue_(self, 3)
            return True
        return False

    def reopen_breaking(self):
        self.d.click_image('close.1334x750.png', timeout=5.0)
        self.d.click_image('break_icon.1334x750.png', timeout=5.0)
        self.d.click_image('public_tab.1334x750.png', timeout=5.0)
        time.sleep(2)

    @log("切换目标阴阳寮")
    def __choose_group(self):
        if self.d.exists('no_target.1334x750.png'):
            return -1
        x, y = self.position.get('first_target')
        self.target = 1 if self.target == 3 else (self.target + 1)
        self.d.click(x, y * self.target)
        time.sleep(1)
        return self.target

    @log("找到目标")
    def __find_under_level(self):
        self.d.keep_screen()
        for i in range(self.level):
            img = 'level_' + str(i) + '.1334x750.png'
            if self.d.click_nowait(img, method='color', threshold=0.9):
                self.d.free_screen()
                time.sleep(0.5 + get_delay())
                self.d.click_image('attack.1334x750.png', timeout=600)
                return i
        self.d.free_screen()
        return -1

    @log2("寻找低等级目标")
    def __find_under_level_scroll(self):
        while True:
            if self.__find_under_level() > -1:
                return True
            else:
                if self.d.exists('broken.1334x750.png'):
                    break
                x1, y1 = self.position.get('break_top')
                x2, y2 = self.position.get('break_bottom')
                self.d.swipe(x2, y2, x1, y1)
                time.sleep(0.5 + get_delay())
        return False

    def breaking(self):
        navigate_to_explore_map(self.d)
        if self.time_ < 0:
            self.d.click_image('break_icon.1334x750.png', timeout=5.0)
            if not self.d.click_image('refresh.1334x750.png', timeout=5.0):
                return False
            self.d.click_image('ok.1334x750.png', timeout=5.0)
            target = self.d.match_images('empty.1334x750.png', timeout=1.0)
            if len(target) < 3:
                return False
            while not self.finish_personal_breaking():
                if not self.d.click_image('empty.1334x750.png', timeout=1.0):
                    break
                time.sleep(0.5 + get_delay())
                self.d.click_image('attack.1334x750.png', timeout=1.0)
                time.sleep(3.5 + get_delay())
                fighting(self)
            return True
        for i in range(3):
            self.last = int(time.time())
            self.reopen_breaking()
            self.__choose_group()
            if self.__find_under_level_scroll():
                time.sleep(4.5 + get_delay())
                if not self.d.exists('level_6.1334x750.png', method='color'):
                    fighting(self)
                    self.times += 1
                else:
                    self.d.click_image('breaking.1334x750.png', timeout=1.0)
            else:
                self.broken[self.target - 1] = 1
                print '第%d个阴阳寮刷完了' % self.target
            self.analysis()
            if self.time_ > 0:
                self.wait()
        while 0 in self.broken and time.time() - self.start < self.time_:
            self.last = int(time.time())
            self.reopen_breaking()
            if self.__choose_group() < 0:
                break
            if self.__find_under_level_scroll():
                self.last = (self.last + int(time.time()) - 15) / 2
                time.sleep(4.5 + get_delay())
                if not self.d.exists('level_6.1334x750.png', method='color'):
                    fighting(self)
                    self.times += 1
                else:
                    self.d.click_image('breaking.1334x750.png', timeout=1.0)
            else:
                self.broken[self.target - 1] = 1
                print '第%d个阴阳寮刷完了' % self.target
            self.analysis()
            self.wait()

    def analysis(self):
        super(Break, self).analysis()
        print '┃%31s%-19s┃' % ('target level: under ', self.level * 10)
        print '┃%25s%-25s┃' % ('broken: ', self.broken)
        print '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
