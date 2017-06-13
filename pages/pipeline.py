# coding=utf-8
import threading
import time

from pages.base_window import Window


class Pipeline(Window):
    MAX_COLUMN = 6
    READY = "images/Gray_pipeline.png"
    GOING = "images/Yellow_pipeline.png"
    PENDING = "images/Blue_pipeline.png"
    FAIL = "images/Red_pipeline.png"
    PASS = "images/Green_pipeline.png"

    def __init__(self, status_list):
        super().__init__()
        self.app.setResizable(canResize=False)
        self.app.setPadding([10, 0])
        self.app.setInPadding([1, 1])
        self.app.setSticky("nsew")
        self.app.setStretch("none")
        self.times_done = 0
        self.status_list = status_list
        self.status = {}
        self.task_running = None
        self.current = ""
        # self.set_pipeline()

    def run_task(self):
        pass

    def stop_task(self):
        pass

    def set_pipeline(self, task_running):
        self.task_running = task_running
        row = 0
        column = 0
        total = 0
        for name in self.status_list:
            if column >= self.MAX_COLUMN:
                total = self.MAX_COLUMN
                row += 3
                column = 0
            self.app.addLabel(name + "Label", name, row, column, 1)
            self.app.addImage(name, self.READY, row + 1, column, 1)
            self.app.addLabel(name, "", row + 2, column, 1)
            column += 1
        if total == 0:
            total = column
        self.app.addLabel("times", "已刷了" + str(self.times_done) + "次", row + 3, total - 2, 2)
        self.app.addButton("停止并返回", self.stop_task, row + 3, 0, 2)
        self.app.setButtonSticky("停止并返回", "")
        self.app.registerEvent(self.update_pipeline)
        self.app.setPollTime(500)
        self.app.go()

    def update_pipeline(self):
        if not self.task_running.isAlive():
            self.set_status(self.current, "fail")
            return
        for name in self.status:
            self.set_status(name, self.status[name])
        self.status = {}

    def set_status(self, name, value):
        if isinstance(value, int):
            if time.time() > value:
                self.app.setImage(name, self.PENDING)
                pending = str(int(600 + value - time.time()))
                self.app.setLabel(name, pending + " 秒后")
            else:
                self.app.setImage(name, self.GOING)
                pending = str(int(time.time() - value))
                self.app.setLabel(name, "剩余 " + pending + " 秒")
        elif value == "going":
            self.current = name
            self.app.setImage(name, self.GOING)
            self.app.setLabel(name, "")
        elif value == "ready":
            self.app.setImage(name, self.READY)
            self.app.setLabel(name, "")
        elif value == "pass":
            self.app.setImage(name, self.PASS)
            self.app.setLabel(name, "")
        elif value == "fail":
            self.app.setImage(name, self.FAIL)
            self.app.setLabel(name, "任务中断")