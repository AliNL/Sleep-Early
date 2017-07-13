# coding=utf-8

from pages import *
from windows.pipelines.pipeline import Pipeline


class BreakTask(Pipeline):
    def __init__(self, times, app, config):
        super().__init__(["突破阴阳寮1", "突破阴阳寮2", "突破阴阳寮3"], app)
        self.times = times
        self.task = Break(self.times, config["l"], 1, config["d"])

    def run_task(self):
        self.status = {"突破阴阳寮1": "going", "突破阴阳寮2": "pending", "突破阴阳寮3": "pending"}
        navigate_to_explore_map(self.task.d)
        for i in range(3):
            self.set_all_status(i + 1, "going", "pending")
            if not self.task.public_breaking(True):
                raise IOError
            self.times_done = self.task.times
            if self.task.time_ > 0:
                self.task.get_next_time()
                pending = int(self.task.next)
                self.set_all_status(i + 1, "pass", pending)
                self.task.wait()
        while 0 in self.task.broken and time.time() - self.task.start < self.task.time_:
            if self.task.target == 3:
                i = 0
            else:
                i = self.task.target
            self.set_all_status(i + 1, "going", "pending")
            if not self.task.public_breaking():
                raise IOError
            self.times_done = self.task.times
            self.task.get_next_time()
            pending = int(self.task.next)
            self.set_all_status(self.task.target, "pass", pending)
            self.task.wait()

    def set_all_status(self, i, status1, status2):
        if i == 1:
            self.status["突破阴阳寮1"] = status1
            self.status["突破阴阳寮2"] = status2
        elif i == 2:
            self.status["突破阴阳寮2"] = status1
            self.status["突破阴阳寮3"] = status2
        else:
            self.status["突破阴阳寮3"] = status1
            self.status["突破阴阳寮1"] = status2
