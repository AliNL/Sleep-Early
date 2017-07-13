# coding=utf-8

from pages import *
from windows.pipelines.pipeline import Pipeline


class GroupTask(Pipeline):
    def __init__(self, times, is_lead, app, config):
        self.is_lead = is_lead
        if self.is_lead:
            super().__init__(["开始战斗", "打怪", "发送邀请"], app)
        else:
            super().__init__(["等待开始", "打怪", "等待邀请"], app)
        self.times = times
        self.task = Group(config["d"])

    def run_task(self):
        for num in range(self.times):
            if self.is_lead:
                t = int(time.time() - 1)
                self.status = {"开始战斗": t, "打怪": "ready", "发送邀请": "ready"}
                if not self.task.start_group_fight():
                    self.status["开始战斗"] = "fail"
                    break
                self.status["开始战斗"] = "pass"
                self.status["打怪"] = "going"
                self.task.group_fight()
                self.status["打怪"] = "pass"
                self.status["发送邀请"] = "going"
                click_ok(self.task.d)
            else:
                t = int(time.time() - 1)
                self.status = {"等待开始": t, "打怪": "ready", "等待邀请": "ready"}
                if not self.task.wait_in_group():
                    self.status["等待开始"] = "fail"
                    break
                self.status["等待开始"] = "pass"
                self.status["打怪"] = "going"
                self.task.group_fight()
                t = int(time.time() - 1)
                self.status["打怪"] = "pass"
                self.status["等待邀请"] = t
                if not click_get(self.task.d):
                    self.status["等待邀请"] = "fail"
                    break
            self.times_done = self.task.times
            self.task.analysis()
