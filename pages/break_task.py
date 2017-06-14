# coding=utf-8
from xml.dom import minidom

from function import *
from pages.pipeline import Pipeline


class BreakTask(Pipeline):
    def __init__(self, times):
        super().__init__(["突破阴阳寮1", "突破阴阳寮2", "突破阴阳寮3"])
        self.times = times
        dom = minidom.parse('./config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        level = int(root.getElementsByTagName('level')[0].firstChild.data)
        self.task = Break(self.times, level, 1, device)

    def run_task(self):
        self.status = {"突破阴阳寮1": "going", "突破阴阳寮2": "pending", "突破阴阳寮3": "pending"}
        navigate_to_explore_map(self.task.d)
        for i in range(3):
            if i == 0:
                self.status = {"突破阴阳寮1": "going", "突破阴阳寮2": "pending", "突破阴阳寮3": "ready"}
            elif i == 1:
                self.status = {"突破阴阳寮1": "ready", "突破阴阳寮2": "going", "突破阴阳寮3": "pending"}
            else:
                self.status = {"突破阴阳寮1": "pending", "突破阴阳寮2": "ready", "突破阴阳寮3": "going"}
            if not self.task.public_breaking(True):
                raise IOError
            self.times_done = self.task.times
            if self.task.time_ > 0:
                self.task.get_next_time()
                pending = self.task.next
                if i == 0:
                    self.status = {"突破阴阳寮1": "pass", "突破阴阳寮2": pending}
                elif i == 1:
                    self.status = {"突破阴阳寮2": "pass", "突破阴阳寮3": pending}
                else:
                    self.status = {"突破阴阳寮3": "pass", "突破阴阳寮1": pending}
                self.task.wait()
        while 0 in self.task.broken and time.time() - self.task.start < self.task.time_:
            if i == 0:
                self.status = {"突破阴阳寮1": "going", "突破阴阳寮2": "pending", "突破阴阳寮3": "ready"}
            elif i == 1:
                self.status = {"突破阴阳寮1": "ready", "突破阴阳寮2": "going", "突破阴阳寮3": "pending"}
            else:
                self.status = {"突破阴阳寮1": "pending", "突破阴阳寮2": "ready", "突破阴阳寮3": "going"}
            if not self.task.public_breaking():
                raise IOError
            self.times_done = self.task.times
            self.task.get_next_time()
            pending = self.task.next
            if i == 0:
                self.status = {"突破阴阳寮1": "pass", "突破阴阳寮2": pending}
            elif i == 1:
                self.status = {"突破阴阳寮2": "pass", "突破阴阳寮3": pending}
            else:
                self.status = {"突破阴阳寮3": "pass", "突破阴阳寮1": pending}
            self.task.wait()
