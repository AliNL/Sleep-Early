# coding=utf-8
from .task import *


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
        self.next = 0

    def get_next_time(self):
        self.next = self.last + 195

    def wait(self):
        while time.time() < self.next:
            get_bonus_task(self.d)
            sys.stdout.write('\r')
            sys.stdout.write('%s -> wait until %s' % (now(), now(self.next)))
            sys.stdout.flush()
        sys.stdout.write('\n')

    @log_underline("突破券充足")
    def if_tickets_enough(self):
        return not self.d.exists('images/no_tickets.1334x750.png', threshold=0.95)

    @log_underline("完成个人结界突破")
    def finish_personal_breaking(self):
        if self.d.wait('images/get_bonus.1334x750.png', threshold=0.9, timeout=5.0):
            continue_(self, 3)
            return True
        return False

    def reopen_breaking(self):
        self.open_breaking_panel()
        self.select_public_breaking_tab()
        time.sleep(2)

    def select_public_breaking_tab(self):
        self.d.click_image('images/public_tab.1334x750.png', timeout=5.0)

    @log("切换目标阴阳寮")
    def __choose_group(self):
        if self.d.exists('images/no_target.1334x750.png'):
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
            img = 'images/level_' + str(i) + '.1334x750.png'
            # targets = self.d.match_all(img, threshold=0.9)
            # for target in targets:
            #     target.rectangle[0]
            if self.d.click_nowait(img, threshold=0.9):
                self.d.free_screen()
                time.sleep(0.5 + get_delay())
                self.d.click_image('images/attack.1334x750.png', timeout=600)
                return i
        self.d.free_screen()
        return -1

    @log2("寻找低等级目标")
    def __find_under_level_scroll(self):
        while True:
            if self.__find_under_level() > -1:
                return True
            else:
                if self.d.exists('images/broken.1334x750.png'):
                    break
                x1, y1 = self.position.get('break_top')
                x2, y2 = self.position.get('break_bottom')
                self.d.swipe(x2, y2, x1, y1)
                time.sleep(0.5 + get_delay())
        return False

    def personal_breaking(self):
        self.open_breaking_panel()
        if not self.refresh_personal_breaking_panel() or not self.validate_empty_targets():
            return False
        while not self.finish_personal_breaking():
            if not self.d.click_image('images/empty.1334x750.png', timeout=1.0):
                break
            time.sleep(0.5 + get_delay())
            self.d.click_image('images/attack.1334x750.png', timeout=1.0)
            time.sleep(3.5 + get_delay())
            fighting(self)
        return True

    def public_breaking(self, start=False):
        self.last = int(time.time())
        self.reopen_breaking()
        if self.__choose_group() < 0:
            return False
        if self.__find_under_level_scroll():
            if not start:
                self.last = (self.last + float(time.time()) - 15) / 2
            time.sleep(4 + get_delay())
            if not self.d.exists('images/level_6.1334x750.png'):
                fighting(self)
                self.times += 1
            else:
                self.d.click_image('images/breaking.1334x750.png', timeout=1.0)
        else:
            self.broken[self.target - 1] = 1
            print('第%d个阴阳寮刷完了' % self.target)
        self.d.click_image('images/close.1334x750.png', timeout=5.0)
        self.analysis()
        return True

    def breaking(self):
        navigate_to_explore_map(self.d)
        if self.time_ < 0:
            return self.personal_breaking()
        for i in range(3):
            if not self.public_breaking(True):
                return False
            if self.time_ > 0:
                self.get_next_time()
                self.wait()
        while 0 in self.broken and time.time() - self.start < self.time_:
            if not self.public_breaking():
                return False
            self.get_next_time()
            self.wait()

    def validate_empty_targets(self):
        target = self.d.match_images('images/empty.1334x750.png', timeout=1.0)
        if len(target) < 3:
            return False
        return True

    def refresh_personal_breaking_panel(self):
        if not self.d.click_image('images/refresh.1334x750.png', threshold=0.9, timeout=5.0):
            return False
        self.d.click_image('images/confirm.1334x750.png', timeout=5.0)
        return True

    def open_breaking_panel(self):
        self.d.click_image('images/break_icon.1334x750.png', timeout=5.0)

    def analysis(self):
        super(Break, self).analysis()
        print('┃%31s%-19s┃' % ('target level: under ', self.level * 10))
        print('┃%25s%-25s┃' % ('broken: ', self.broken))
        print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
