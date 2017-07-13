# coding=utf-8

from pages import *
from windows.pipelines.pipeline import Pipeline


class AutoTask(Pipeline):
    def __init__(self, times, app, config):
        super().__init__(["选择章节", "打怪", "捡宝箱", "打石距", "个人突破", "阴阳寮突破"], app)
        self.times = times
        self.ex = Explore(config["c"], config["d"])
        self.br = Break(-1, config["l"], 1, config["d"])
        self.bp = Break(0, config["l"], 1, config["d"])

    def kill(self):
        self.ex.d = None
        self.br.d = None
        self.bp.d = None

    def run_task(self):
        t = -600
        for num in range(self.times):
            navigate_to_explore_map(self.ex.d)
            if 600 + t - time.time() < 0:
                t = -600
            self.status = {"选择章节": "going",
                           "打怪": "ready",
                           "捡宝箱": "ready",
                           "打石距": "ready",
                           "个人突破": t + 600,
                           "阴阳寮突破": t + 600}
            if self.ex.is_pl_not_enough():
                self.status["选择章节"] = "fail"
                break
            self.ex.choose_chapter()
            self.status["选择章节"] = "pass"
            self.status["打怪"] = "going"
            self.ex.exploring_fight()
            self.status["打怪"] = "pass"
            self.status["捡宝箱"] = "going"
            self.ex.get_small_box()
            self.ex.get_big_box()
            self.status["捡宝箱"] = "pass"
            self.status["打石距"] = "going"
            # if self.ex.found_shi_ju():
            #     self.ex.d.delay(5 * 60)
            if 600 + t - time.time() < 0:
                if self.br.if_tickets_enough():
                    self.status["打石距"] = "pass"
                    self.status["个人突破"] = "going"
                    self.br.breaking()
                t = int(time.time())
                self.status["个人突破"] = "pass"
                self.status["阴阳寮突破"] = "going"
                self.bp.breaking()
            self.times_done = self.ex.times
            self.ex.analysis()
