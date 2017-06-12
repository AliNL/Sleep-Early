# coding=utf-8
import os

from auto import Auto
from base_window import Window
import config


class TaskChoose(Window):
    MESSAGE = {"自动": "任务详情：一直刷单人探索，每10分钟刷个人结界突破（直到胜利3次或打完）和阴阳寮结界突破（3个）",
               "单人探索": "任务详情：一直刷单人探索，直到达到次数或体力用尽",
               "组队探索": "任务详情：一直刷组队探索，直到达到次数或体力用尽，对方1分钟未响应时停止",
               "结界突破": "任务详情：每10分钟刷个人结界突破（直到胜利3次或打完）和阴阳寮结界突破（3个），直到达到时间或刷完",
               "组队副本": "任务详情：一直刷组队御魂或觉醒，直到达到次数或体力用尽，对方1分钟未响应时停止"}

    def go_back(self, btn):
        if os.path.exists('config.xml'):
            os.remove('config.xml')
        self.app.stop()
        config.Config().start_config()

    def set_message(self, name):
        self.app.setMessage("message", self.MESSAGE[name])

    def get_options(self, name):
        task_type = self.app.getOptionBox(name)
        if task_type in ["自动", "单人探索"]:
            self.app.showCheckBox("自动打石距(还没做好)")
        else:
            self.app.hideCheckBox("自动打石距(还没做好)")
        if task_type == "结界突破":
            self.app.setLabel("times", "刷多少小时：")
        else:
            self.app.setLabel("times", "刷多少把：")
        if task_type in ["组队探索", "组队副本"]:
            self.app.showCheckBox("我是队长")
        else:
            self.app.hideCheckBox("我是队长")

        self.set_message(task_type)

    def start_task(self, btn):
        task_type = self.app.getOptionBox("task")
        times = int(float(self.app.getEntry("times")))
        is_lead = self.app.getCheckBox("我是队长")
        self.app.stop()
        if task_type == "自动":
            Auto(times).start()

    def choose_task(self):
        self.app.addLabel("task", "选择任务：", 0, 0, 1)
        self.app.setLabelAlign("task", "right")
        self.app.addOptionBox("task", ["自动", "单人探索", "组队探索", "结界突破", "组队副本"], 0, 1, 1)
        self.app.setOptionBoxWidth("task", 10)
        self.app.setOptionBoxSticky("task", "w")
        self.app.addLabel("times", "刷多少把：", 0, 2, 1)
        self.app.setLabelAlign("times", "right")
        self.app.addNumericEntry("times", 0, 3, 1)
        self.app.setEntryWidth("times", 10)
        self.app.setEntrySticky("times", "w")
        self.app.addEmptyMessage("message", 1, 0, 4)
        self.app.setMessageWidth("message", 400)
        self.app.addCheckBox("自动打石距(还没做好)", 2, 0, 2)
        self.app.setCheckBoxSticky("自动打石距(还没做好)", "")
        self.app.disableCheckBox("自动打石距(还没做好)")
        self.app.addCheckBox("我是队长", 2, 0, 2)
        self.app.setCheckBoxSticky("我是队长", "")

        self.get_options("task")
        self.app.addButton("更改默认设置", self.go_back, 3, 0, 2)
        self.app.setButtonSticky("更改默认设置", "")
        self.app.addButton(" 开始 ", self.start_task, 3, 2, 2)
        self.app.setButtonSticky(" 开始 ", "")

        self.app.setOptionBoxChangeFunction("task", self.get_options)

        self.app.go()
