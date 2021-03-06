# coding=utf-8

from .task import *


class Explore(Task):
    def __init__(self, chapter=16, device='android'):
        if not 0 < chapter < 24:
            raise IOError("Invalid chapter number!!!")
        super(Explore, self).__init__(device)
        self.name = 'Explore'
        self.chapter = chapter
        self.monster_killed = 0
        self.small_box = 0
        self.big_box = 0
        self.stop_reason = 'task completed'

    @log2("选择探索章节")
    def choose_chapter(self):
        image_name = img('C' + str(self.chapter))
        for t in range(-5, 5):
            if self.d.click_image(image_name, safe=True, threshold=0.9, timeout=1.0):
                time.sleep(1 + get_delay())
                if self.d.click_image(img('explore_icon')):
                    time.sleep(3 + get_delay())
                    return self.chapter
            else:
                x1, y1 = self.position.get('chapter_top')
                x2, y2 = self.position.get('chapter_bottom')
                if t > 0:
                    self.d.swipe(x2, y2, x1, y1)
                else:
                    self.d.swipe(x1, y1, x2, y2)
            time.sleep(1 + get_delay())

    @log2("打小怪")
    def __fight_monster(self):
        for i in range(-8, 8):
            if self.d.click_image(img('monster_icon'), safe=True, threshold=0.9, timeout=1.0):
                time.sleep(2.5 + get_delay())
                if is_exploring(self.d):
                    if self.d.exists(img('buying_energy')):
                        self.analysis()
                        return False
                    continue
                fighting(self)
                self.monster_killed += 1
                return True
            else:
                direction = 'left' if i > 0 else 'right'
                self.d.click(*self.position.get(direction))
                time.sleep(1.5 + get_delay())
        return False

    @log2("打boss")
    def __fight_boss(self, delay_):
        if self.d.click_image(img('boss_icon'), safe=True, threshold=0.85, timeout=5.0, delay=delay_):
            time.sleep(2.5 + get_delay())
            if is_exploring(self.d):
                if self.d.exists(img('buying_energy')):
                    # os.system('say -v Ting-Ting "体力不足"')
                    self.analysis()
                    return False
            fighting(self)
            self.times += 1
            return True
        return False

    def exploring_fight(self, delay=0):
        while not self.__fight_boss(delay):
            self.__fight_monster()
        while self.__fight_boss(delay):
            pass

    @log2("捡小宝箱")
    def get_small_box(self):
        for i in range(3):
            if in_explore_map(self.d):
                return
            boxes = self.d.match_all(img('small_treasure_box'), threshold=0.9)
            if boxes:
                for box in boxes:
                    self.d.click(*box['result'])
                    time.sleep(0.5 + get_delay())
                    continue_(self, 1)
                    self.small_box += 1
            time.sleep(1 + get_delay())
        raise AssertionError

    @log("捡大宝箱")
    def get_big_box(self):
        for i in range(2):
            if self.d.click_image(img('big_treasure_box'), safe=True, timeout=1.0):
                time.sleep(0.5 + get_delay())
                continue_(self, 3)
                self.big_box += 1
                return True
            else:
                time.sleep(get_delay())
        return False

    @log("查找石距")
    def found_shi_ju(self):
        self.d.keep_screen()
        if self.d.exists(img('shi_ju')):
            self.stop_reason = 'shi ju found'
            self.analysis()
            return True
        return False

    @log("是否体力不足")
    def is_pl_not_enough(self):
        if self.d.exists(img('no_enough_pl'), threshold=0.95):
            self.stop_reason = 'energy not enough'
            self.analysis()
            return True
        return False

    def analysis(self):
        self.d.free_screen()
        super(Explore, self).analysis()
        # print('┃%25s%-25s┃' % ('monster killed: ', self.monster_killed))
        # print('┃%25s%-25s┃' % ('small box: ', self.small_box))
        # print('┃%25s%-25s┃' % ('big box: ', self.big_box))
        # print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
