# coding=utf-8
from xml.dom import minidom

from function import *
from pipeline import Pipeline


class AutoTask(Pipeline):
    def __init__(self, times):
        super().__init__(["选择章节", "打怪", "捡宝箱", "打石距", "个人突破", "阴阳寮突破"])
        self.times = times
        self.status = {}

    @staticmethod
    def get_pending_time(t):
        if time.time() - t < 600:
            return str(int(600 - time.time() + t))
        else:
            return "ready"

    def start(self):
        dom = minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        level = int(root.getElementsByTagName('level')[0].firstChild.data)
        chapter = int(root.getElementsByTagName('chapter')[0].firstChild.data)
        ex = Explore(chapter, device)
        br = Break(-1, level, 1, device)
        bp = Break(0, level, 1, device)
        t = 0
        for num in range(self.times):
            navigate_to_explore_map(ex.d)
            self.status = {"选择章节": "going",
                           "打怪": "ready",
                           "捡宝箱": "ready",
                           "打石距": "ready",
                           "个人突破": self.get_pending_time(t),
                           "阴阳寮突破": self.get_pending_time(t)}
            if ex.is_pl_not_enough():
                break
            ex.choose_chapter()
            self.status = {"选择章节": "pass", "打怪": "going", "个人突破": self.get_pending_time(t),
                           "阴阳寮突破": self.get_pending_time(t)}
            ex.exploring_fight()
            self.status = {"打怪": "pass", "捡宝箱": "going", "个人突破": self.get_pending_time(t),
                           "阴阳寮突破": self.get_pending_time(t)}
            ex.get_small_box()
            ex.get_big_box()
            self.status = {"捡宝箱": "pass", "打石距": "going", "个人突破": self.get_pending_time(t),
                           "阴阳寮突破": self.get_pending_time(t)}
            if ex.found_shi_ju():
                ex.d.delay(5 * 60)
            if time.time() - t > 600:
                if br.if_tickets_enough():
                    self.status = {"打石距": "pass", "个人突破": "going", "阴阳寮突破": self.get_pending_time(t)}
                    br.breaking()
                t = time.time()
                self.status = {"个人突破": "pass", "阴阳寮突破": "going"}
                bp.breaking()
            ex.analysis()

