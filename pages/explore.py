# coding=utf-8
from xml.dom import minidom

from function import Explore, navigate_to_explore_map
from pages.pipeline import Pipeline


class ExploreTask(Pipeline):
    def __init__(self, times):
        super().__init__(["选择章节", "打怪", "捡宝箱", "打石距"])
        self.times = times
        dom = minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        chapter = int(root.getElementsByTagName('chapter')[0].firstChild.data)
        self.task = Explore(chapter, device)

    def run_task(self):
        for num in range(self.times):
            self.status = {"选择章节": "going", "打怪": "ready", "捡宝箱": "ready", "打石距": "ready"}
            navigate_to_explore_map(self.task.d)
            if self.task.is_pl_not_enough():
                break
            self.task.choose_chapter()
            self.status = {"选择章节": "pass", "打怪": "going"}
            self.task.exploring_fight()

            self.status = {"打怪": "pass", "捡宝箱": "going"}
            self.task.get_small_box()
            self.task.get_big_box()
            self.status = {"捡宝箱": "pass", "打石距": "going"}
            if self.task.found_shi_ju():
                self.task.d.delay(5 * 60)
            self.times_done = self.task.times
            self.task.analysis()
