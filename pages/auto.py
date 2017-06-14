# coding=utf-8
from xml.dom import minidom

from pages.pipeline import Pipeline
from function import *


class AutoTask(Pipeline):
    def __init__(self, times):
        super().__init__(["选择章节", "打怪", "捡宝箱", "打石距", "个人突破", "阴阳寮突破"])
        self.times = times
        dom = minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        level = int(root.getElementsByTagName('level')[0].firstChild.data)
        chapter = int(root.getElementsByTagName('chapter')[0].firstChild.data)
        self.ex = Explore(chapter, device)
        self.br = Break(-1, level, 1, device)
        self.bp = Break(0, level, 1, device)

    def kill(self):
        self.ex.d = None
        self.br.d = None
        self.bp.d = None

    def run_task(self):
        t = -600
        for num in range(self.times):
            navigate_to_explore_map(self.ex.d)
            self.status = {"选择章节": "going",
                           "打怪": "ready",
                           "捡宝箱": "ready",
                           "打石距": "ready",
                           "个人突破": t + 600,
                           "阴阳寮突破": t + 600}
            if self.ex.is_pl_not_enough():
                self.status = {"选择章节": "fail"}
                break
            self.ex.choose_chapter()
            self.status = {"选择章节": "pass", "打怪": "going", "个人突破": t + 600,
                           "阴阳寮突破": t + 600}
            self.ex.exploring_fight()
            self.status = {"打怪": "pass", "捡宝箱": "going", "个人突破": t + 600,
                           "阴阳寮突破": t + 600}
            self.ex.get_small_box()
            self.ex.get_big_box()
            self.status = {"捡宝箱": "pass", "打石距": "going", "个人突破": t + 600,
                           "阴阳寮突破": t + 600}
            # if self.ex.found_shi_ju():
            #     self.ex.d.delay(5 * 60)
            if 600 + t - time.time() < 0:
                if self.br.if_tickets_enough():
                    self.status = {"打石距": "pass", "个人突破": "going", "阴阳寮突破": t + 600}
                    self.br.breaking()
                t = time.time()
                self.status = {"个人突破": "pass", "阴阳寮突破": "going"}
                self.bp.breaking()
            self.times_done = self.ex.times
            self.ex.analysis()
