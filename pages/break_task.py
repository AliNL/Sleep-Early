# coding=utf-8
from xml.dom import minidom

from function import *
from pages.pipeline import Pipeline


class BreakTask(Pipeline):
    def __init__(self, times):
        super().__init__(["突破阴阳寮1", "突破阴阳寮2", "突破阴阳寮3"])
        self.times = times

    def run_task(self):
        dom = minidom.parse('config.xml')
        root = dom.documentElement
        device = root.getElementsByTagName('device')[0].firstChild.data
        level = int(root.getElementsByTagName('level')[0].firstChild.data)

        task = Break(self.times, level, 1, device)
        self.status = {"突破阴阳寮1": "going", "突破阴阳寮2": "pending", "突破阴阳寮3": "pending"}
        navigate_to_explore_map(task.d)
        for i in range(3):
            if i == 0:
                self.status = {"突破阴阳寮1": "going", "突破阴阳寮2": "pending", "突破阴阳寮3": "ready"}
            elif i == 1:
                self.status = {"突破阴阳寮1": "ready", "突破阴阳寮2": "going", "突破阴阳寮3": "pending"}
            else:
                self.status = {"突破阴阳寮1": "pending", "突破阴阳寮2": "ready", "突破阴阳寮3": "going"}
            if not task.public_breaking(True):
                raise IOError
            self.times_done = task.times
            if task.time_ > 0:
                pending = task.get_next_time()
                if i == 0:
                    self.status = {"突破阴阳寮1": "pass", "突破阴阳寮2": pending}
                elif i == 1:
                    self.status = {"突破阴阳寮2": "pass", "突破阴阳寮3": pending}
                else:
                    self.status = {"突破阴阳寮3": "pass", "突破阴阳寮1": pending}
                task.wait()
        while 0 in task.broken and time.time() - task.start < task.time_:
            if i == 0:
                self.status = {"突破阴阳寮1": "going", "突破阴阳寮2": "pending", "突破阴阳寮3": "ready"}
            elif i == 1:
                self.status = {"突破阴阳寮1": "ready", "突破阴阳寮2": "going", "突破阴阳寮3": "pending"}
            else:
                self.status = {"突破阴阳寮1": "pending", "突破阴阳寮2": "ready", "突破阴阳寮3": "going"}
            if not task.public_breaking():
                raise IOError
            self.times_done = task.times
            task.get_next_time()
            if i == 0:
                self.status = {"突破阴阳寮1": "pass", "突破阴阳寮2": pending}
            elif i == 1:
                self.status = {"突破阴阳寮2": "pass", "突破阴阳寮3": pending}
            else:
                self.status = {"突破阴阳寮3": "pass", "突破阴阳寮1": pending}
            task.wait()
