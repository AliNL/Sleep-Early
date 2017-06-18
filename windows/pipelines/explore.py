# coding=utf-8
from xml.dom import minidom

from pages import Explore, navigate_to_explore_map
from windows.pipelines.pipeline import Pipeline


class ExploreTask(Pipeline):
    def __init__(self, times, app):
        super().__init__(["选择章节", "打怪", "捡宝箱", "打石距"], app)
        self.times = times
        from pages.steps.path_manager import cfg
        dom = minidom.parse(cfg())
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        chapter = int(root.getElementsByTagName('chapter')[0].firstChild.data)
        self.task = Explore(chapter, device)

    def run_task(self):
        for self.times_done in range(self.times):
            self.status = {"选择章节": "going", "打怪": "ready", "捡宝箱": "ready", "打石距": "ready"}
            navigate_to_explore_map(self.task.d)
            if self.task.is_pl_not_enough():
                break
            self.task.choose_chapter()
            self.status["选择章节"] = "pass"
            self.status["打怪"] = "going"
            self.task.exploring_fight()
            self.status["打怪"] = "pass"
            self.status["捡宝箱"] = "going"
            self.task.get_small_box()
            self.task.get_big_box()
            self.status["捡宝箱"] = "pass"
            self.status["打石距"] = "going"
            # if self.task.found_shi_ju():
            #     self.task.d.delay(5 * 60)
            # self.task.analysis()
